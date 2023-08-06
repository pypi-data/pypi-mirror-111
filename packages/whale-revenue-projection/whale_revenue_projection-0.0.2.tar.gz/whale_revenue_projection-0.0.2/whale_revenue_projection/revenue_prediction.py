import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from enum import Enum
from datetime import date
from typing import Optional
from .get_ltv import get_ltv
from .get_survival import get_survival


class populationType(Enum):
    all = "all"
    bottom = "bottom-95-percent"


def revenue_prediction(
    n: int,
    data_type: str,
    id: int,
    pop: Optional[populationType] = "all",
    server: Optional[str] = "Willy",
) -> pd.DataFrame():
    """
    n = Number of forecasted users
    data = campaign/product/sponsor
    id = campaign_id/product_id/sponsor_id
    pop = population type
    """

    # Reading the data
    data = get_ltv(server=server, data_type=data_type, id=id, pop=pop)

    ##########
    ### Use the LTV, the Survival rate and the number of Users to have estimates of revenue
    ##########

    ######
    # First step : get the survival rate and see the evolution of the population
    survival = get_survival(server=server, data_type=data_type, id=id, pop=pop)

    ####
    # Population Chuun
    pop_decay = pd.DataFrame()
    survive = survival["Surv prob"]
    # survive = pd.concat(
    #     [pd.Series([1]), survive]
    # )  # assuming that the first week, all the users survive
    # survive = survive[:-1]  # Removing the last value as the series would be too long.

    for i in survive:
        n = n * i
        values = {"SOURCE_ID": id, "pop_decay": n}
        pop_decay = pop_decay.append(values, ignore_index=True)

    #####
    # Second is to look at what additional revenue we have at each week

    diff = data["cumsum"].diff()
    diff.iloc[0] = data["cumsum"].iloc[0]
    diff = diff[0 : len(survive)]
    diff = diff.reset_index(drop=True)
    pop_decay["revenue"] = diff * pop_decay["pop_decay"]
    pop_decay["cumsum"] = pop_decay["revenue"].cumsum()
    pop_decay = pop_decay.reset_index().rename(columns={"index": "T"})
    pop_decay = pop_decay.iloc[:7]

    return pop_decay
