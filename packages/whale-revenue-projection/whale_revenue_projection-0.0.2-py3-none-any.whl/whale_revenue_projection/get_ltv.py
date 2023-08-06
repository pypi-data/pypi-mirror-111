import os
import pandas as pd

from typing import Optional
from whale_back_bone.mysql_connection.db_connections import db_connections as db


def get_ltv(
    data_type: str, id: int, pop: str = "all", server: Optional[str] = "Willy"
) -> pd.DataFrame:
    """
    Function that returns the LTV data for a specific source and source id
    """

    connection = db().create_external_connection(
        host=os.getenv(f"{server.upper()}_HOST"),
        port=3306,
        dbname="falconreports",
        user=os.getenv(f"{server.upper()}_USERNAME"),
        password=os.getenv(f"{server.upper()}_PASSWORD"),
    )

    query = f"""
            SELECT
                *
            FROM
                falconreports.ltv_all_time
            WHERE
                source_type = "{data_type}"
                AND source_id = "{id}"
                AND population = "{pop}"
            """

    ltv = db().query_to_db(connection=connection, query=query)

    return ltv


if __name__ == "__main__":
    truc = get_ltv("campaign", "666", "bottom-95-percent")

    print(truc.head())
