from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
from datetime import datetime, timedelta
from datetime import date
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    execute_date = kwargs.get("execution_date").date()
    day_before_execute_date = execute_date - timedelta(days=1)

    print(f'execute date is {execute_date} and the day before is {day_before_execute_date}')


    date_input:str = day_before_execute_date.strftime("%Y-%m-%d")
    
    date_to_process_slash:str = date_input.replace('-', '/')

    bucket_name = 'data-engineering-zoomcamp-2024-project'
    object_key = f'daily/{date_to_process_slash}/{date_input}.csv'

    print(f'cloud storage object key: {object_key}')

    return GoogleCloudStorage.with_config(ConfigFileLoader(
        config_path, config_profile)).load(
        bucket_name,
        object_key,
        'csv'
    )


def is_numeric(x):
    try:
        pd.to_numeric(x)
        return True
    except (TypeError, ValueError):
        return False

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

    # assert stationId field exists and not null or empty
    assert output['stationId'].isna().any() == False , "Expect stationId is not null or empty"

    # assert timestamp field exists and not null or empty
    assert output['timestamp'].isna().any() == False , "Expect timestamp is not null or empty"

    # assert temperature field is numberic if exists
    assert output['temperature'].apply(is_numeric).all() == True, "Expect temperature to be nuneric if exists"
    
