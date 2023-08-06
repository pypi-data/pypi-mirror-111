import os
import pandas as pd

from typing import Optional
from whale_back_bone.mysql_connection.db_connections import db_connections as db


def get_survival(
    data_type: str, id: int, pop: str = "all", server: Optional[str] = "Willy"
) -> pd.DataFrame:
    """
    Function that returns the Survival rate for a specific source and source id
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
                falconreports.survival_all_time
            WHERE
                source_type = "{data_type}"
                AND source_id = "{id}"
                AND population = "{pop}"
            """

    survival = db().query_to_db(connection=connection, query=query)

    return survival


if __name__ == "__main__":
    truc = get_survival("campaign", "666", "bottom-95-percent")

    print(truc.head())
