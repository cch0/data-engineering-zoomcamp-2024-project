from datetime import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # filter out rows where 'temperature' is null
    data = data.dropna(subset=['temperature'])

    # add 'date', 'hour' and 'minute' colunns using string from 'timestamp' column
    data['date'] = data['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d'))
    data['hour'] = data['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').strftime('%H'))
    data['minute'] = data['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').strftime('%M'))

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

    assert output['date'].isna().any() == False, "date column is undefined" 
    assert output['hour'].isna().any() == False, "hour column is undefined" 
    assert output['minute'].isna().any() == False, "minute column is undefined" 

