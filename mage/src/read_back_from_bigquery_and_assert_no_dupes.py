from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_big_query(*args, **kwargs):
    # construct table id from env variables
    gcp_project_id=os.environ.get('GCP_PROJECT')
    bigquery_dataset=os.environ.get('BIGQUERY_DATASET')
    bigquery_table='table1'
    table_id = f'{gcp_project_id}.{bigquery_dataset}.{bigquery_table}'


    query = f'select * from {table_id}'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)


@test
def test_output(output, *args) -> None:
    
    assert output is not None, 'The output is undefined'

    # identify duplicate rows based on stationId, date, hour and minute columns
    duplicated_values = output.duplicated(subset=['stationId', 'date', 'hour', 'minute'], keep='last')
    duplicate_rows = output[duplicated_values]
    
    assert duplicate_rows is not None, 'expect duplicate_rows to be non None'
    assert duplicate_rows.shape[0] == 0, 'expect no deplicate rows'

