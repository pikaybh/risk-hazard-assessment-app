# %% Internal Modules
from . import vectordb
from . import search
from . import api_keys
# External Modules
import pandas as pd
import numpy as np
from tabulate import tabulate
import logging

# Root 
logger_name = 'utils'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# File Handler
file_handler = logging.FileHandler(f'logs/{logger_name}.log', encoding='utf-8-sig')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(r'%(message)s'))
logger.addHandler(stream_handler)

def get_df(file_dir : str) -> pd.DataFrame:
    """
    Reads an Excel file from the given path, processes it, and returns a DataFrame.

    The function performs the following steps:
    1. Reads the Excel file into a DataFrame.
    2. Drops the first and second columns.
    3. Fills NaN values with the value from the cell directly above.
    4. Logs the DataFrame using a tabulated format.

    :param file_dir: The path to the Excel file.
    :type file_dir: str
    :return: The processed DataFrame.
    :rtype: pd.DataFrame

    Example:
        >>> df = get_df('path/to/your/excel_file.xlsx')
    """
    _df: pd.DataFrame = pd.read_excel(file_dir)  # Read the Excel file into a DataFrame
    _df.drop(columns=[_df.columns[0], _df.columns[1]], inplace=True)  # Drop the first and second columns
    _df.fillna(method='ffill', inplace=True)  # Fill NaN values with the value from the cell directly above
    logger.info(tabulate(_df, headers='keys', tablefmt='psql'))  # Log the DataFrame in a tabulated format
    return _df  # Return the processed DataFrame

def main() -> None:
    df : pd.DataFrame = get_df(r"docs\codenaming.xlsx")

# Main
if __name__ == '__main__':
    main()

# %%
