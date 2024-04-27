import pandas as pd
from pandas import DataFrame
import math
from datetime import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# def transform_datatypes(df: DataFrame):
#     return df

@transformer
def transform_df(df: DataFrame, *args, **kwargs) -> DataFrame:
    df['Area'] = df['Area'].str.replace(' m²', '')
    df['Area'] = df['Area'].str.replace(',', '.')
    df['Area'] = df['Area'].str.replace('\xa0', '', regex=True)
    df['Area'] = df['Area'].astype(float).fillna(0.0)

    df = df.astype(
        {
            "ID": int,
            "Area": float,
            "Price": float
            # "Rooms": int,
            # "floor": int,
            # "rent": float,
            # "building year": int    
        }
    )

    df['Price per m2'] = (df['Price'] / df['Area']).round(1)
    

    return df
    
    # =transform_datatypes(df)


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
