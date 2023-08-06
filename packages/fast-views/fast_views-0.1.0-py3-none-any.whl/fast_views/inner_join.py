import sys
from operator import add
import logging
from functools import reduce
from typing import List
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def inner_join(dataframes: List[pd.DataFrame])-> pd.DataFrame:
    """
    Join a list of dataframes with time-unit indexing
    """

    start,end = 0,sys.maxsize
    strides = np.zeros((len(dataframes),2))
    current_stride = 0
    for idx,df in enumerate(dataframes):
        if not df.index.is_monotonic:
            df.sort_index(inplace = True)

        start = max(start,df.index[0][0])
        end = min(end,df.index[-1][0])
        strides[idx,:] = [current_stride, current_stride + df.shape[1]]
        current_stride += df.shape[1]

    rows = dataframes[0].loc[start:end,:].shape[0]
    cols = sum(map(lambda df: df.shape[1], dataframes))

    model = dataframes[0].loc[start:end]

    mat = np.full((rows,cols), np.NaN)

    for idx,df in enumerate(dataframes):
        col_start, col_end= (int(i) for i in strides[idx,:])
        mat[:, col_start:col_end] = df.loc[start:end,:].values

    columns = reduce(add, map(lambda df: list(df.columns), dataframes))
    return pd.DataFrame(
            mat,
            columns = columns,
            index = model.index
            )
