from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
from datetime import date
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'data-engineering-zoomcamp-2024-project'
    object_key = 'daily/2024/03/22/2024-03-22.csv'

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
    
