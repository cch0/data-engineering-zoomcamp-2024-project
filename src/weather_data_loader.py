import requests
import json
from google.cloud import storage
from datetime import datetime

# station_ids = ['ASHW1', 'ENCW1', 'FTAW1']

station_ids = ['ASHW1']

class WeatherDataLoader:

    storage_client: storage.Client=None
    bucket_name:str=None
    bucket:storage.Bucket=None
    credentials_file:str=None


    def create_storage_client(self):
        return storage.Client.from_service_account_json(self.credentials_file)


    def get_bucket(self):
        return self.storage_client.bucket(self.bucket_name)


    def upload_to_bucket(self, content: str, blob_name: str):
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(content)


    def tick(self):

        for station_id in station_ids:
            # station specific url
            url = 'https://api.weather.gov/stations/' + station_id + '/observations/latest'

            # send request
            response = requests.get(url)

            # get the response in dict
            response_json: dict = response.json()

            # we like to extract timestamp field which is in properties.timestamp field
            if 'properties' in response_json:
                properties = response_json['properties']

                if 'timestamp' in properties:
                    timestamp_string = properties['timestamp']

                    # based on the timestamp, determine the blob name
                    blob_name = self.generate_blob_name(station_id, timestamp_string)
                    print('blob name is', blob_name)

                    # convert from dict to string as storage client can process string without
                    # us having to store it to local file then upload.
                    content:str = json.dumps(response_json)

                     # Upload the file to the bucket
                    self.upload_to_bucket(content, blob_name)
                else:
                    print('No timestamp field found in the response for station', station_id)
            else:
                print('No properties field found in the response for station', station_id)


    def generate_blob_name(self, station_id: str, timestamp_string: str):
        # example: 2024-03-21T11:07:00+00:00
        timestamp = datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S%z')
        # print(type(timestamp))

        # construct blob name in GCS
        blob_name = 'raw/{year}/{month}/{day}/{hour}_{minute}_{station_id}.json'.format(
            year=timestamp.year,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute,
            station_id=station_id
            )

        return blob_name



    def init(self):
        self.storage_client = self.create_storage_client()
        self.bucket = self.get_bucket()


def main():
    loader=WeatherDataLoader()
    loader.credentials_file='./google_credential.json'
    loader.bucket_name='data-engineering-zoomcamp-2024-project'
    loader.init()
    loader.tick()



if __name__ == "__main__":
    main()

