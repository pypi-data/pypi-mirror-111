import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from enum import Enum
from typing import Optional
from .revenue_prediction import revenue_prediction, populationType
from whale_back_bone.mysql_connection.db_connections import db_connections as db


def validation(
    server: str,
    id_number: int,
    data_type: str,
    number_spenders:Optional[int] = None,
    pop: Optional[populationType] = "all",
    creds_path: Optional[str] = None,
    saving: Optional[bool] = False,
    show: Optional[bool] = False
) -> pd.DataFrame():

    """
    Function that forecast on the next 6 weeks the cumulative revenue
    for a specified number of spenders.
    """

    if creds_path:
        with open(creds_path) as f:
            creds = json.load(f)

        production = creds["Prod"]

        conn = db().create_external_connection(
            host=production["host"],
            port=production["port"],
            dbname="falconstats",
            user=production["user"],
            password=production["password"],
        )
    else:
        host = os.getenv(f"{server.upper()}_HOST")
        user = os.getenv(f"{server.upper()}_USERNAME")
        password = os.getenv(f"{server.upper()}_PASSWORD")

        conn = db().create_external_connection(
            host=host,
            port=3306,
            dbname="falconstats",
            user=user,
            password=password,
        )

    # pull 12 dates

    dates = [
        "2019-05-27",
        "2019-07-29",
        "2019-09-30",
        "2019-12-02",
        "2020-01-27",
        "2020-03-30",
        "2020-06-01",
        "2020-07-27",
        "2020-09-28",
        "2020-11-30",
        "2021-02-01",
        "2021-03-29",
    ]

    # look at each first week and extract the number of starting user

    average_cohort = pd.DataFrame()

    # track them on 5 weeks and their revenue

    for date in dates:
        cohort_query = f"""
                        SELECT
                            YEAR(transDate) AS year_number,
                            WEEK(transDate) AS week_number,
                            COUNT(DISTINCT ds.foreignUserID) user_count,
                            SUM(ds.netAmt) AS revenue
                        FROM
                            falconstats.dailytransactions AS ds
                            INNER JOIN falconstats.summary_spenders AS ss ON ss.foreignUserID = ds.foreignUserID
                        WHERE
                            ss.signupDate BETWEEN "{date}" AND "{date}" + INTERVAL 7 DAY
                            AND transDate BETWEEN "{date}" AND "{date}" + INTERVAL 49 DAY
                            AND ds.{data_type}_id = {id_number}
                        GROUP BY
                            YEAR(transDate),
                            WEEK(transDate)
                        ORDER BY
                            YEAR(transDate),
                            WEEK(transDate)
                        """
        cohort = db().query_to_db(connection=conn, query=cohort_query)

        if len(cohort) > 7:
            cohort = cohort[:7]

            cohort["week_to_aggregate"] = [1, 2, 3, 4, 5, 6, 7]

            cohort["cohort"] = date

            average_cohort = average_cohort.append(cohort)
        else:
            pass

    # average both the number of first users and also the weekly evolution

    average_cohort.drop(columns=["week_number", "year_number"], inplace=True)

    average = average_cohort.groupby("week_to_aggregate").mean()

    average = average.reset_index()

    cumsum_average = average["revenue"].cumsum()

    # the the first week average to generate a prediction

    if number_spenders:
        number = number_spenders
    else:
        number = round(average["user_count"][0], 1)

    population = revenue_prediction(
        n=number, data_type=data_type, id=id_number, pop=pop
    )

    # Plot the projected revenue and churn to the averaged revenue and churn.

    difference = population["cumsum"] - cumsum_average

    population["cumsum_higher_range"] = population["cumsum"] + abs(difference)

    population["cumsum_lower_range"] = population["cumsum"] - abs(difference)

    population[population < 0] = 0

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=population["T"],
            y=population["cumsum"],
            line_color="green",
            name="Prediction",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=population["T"],
            y=population["cumsum_higher_range"],
            line=dict(color="red", width=4, dash="dash"),
            name="high",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=population["T"],
            y=population["cumsum_lower_range"],
            line=dict(color="blue", width=4, dash="dash"),
            name="low",
        )
    )
    fig.update_traces(mode="lines")

    fig.update_layout(
        height=800,
        title_text=f'Revenue projections for {average["user_count"][0]} average user for {data_type}_id {id_number}',
    )
    if saving:
        os.makedirs("./data/", exist_ok=True)
        fig.write_html(f"./data/revenue_validation_{data_type}_id_{id_number}.html")
    elif show:
        fig.show()
    print(f"Done with {data_type}_id {id_number}")
    return population
