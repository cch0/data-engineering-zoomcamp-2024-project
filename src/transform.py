import json
import pandas as pd
from google.cloud import storage
from datetime import datetime
from datetime import date
from google.cloud.storage import Blob
from google.cloud import storage
from datetime import datetime

class Transform:
    storage_client: storage.Client=None
    bucket_name:str=None
    bucket:storage.Bucket=None
    credentials_file:str=None

    columns = [ 'stationId', 'timestamp', 'temperature', 'dewpoint',
               'windDirection', 'windSpeed', 'windGust', 'barometricPressure',
               'seaLevelPressure', 'visibility', 'maxTemperatureLast24Hours',
               'minTemperatureLast24Hours', 'precipitationLast3Hours', 'relativeHumidity',
               'windChill', 'heatIndex', 'latitude', 'longitude']


    def create_storage_client(self):
        return storage.Client.from_service_account_json(self.credentials_file)


    def get_bucket(self):
        return self.storage_client.bucket(self.bucket_name)


    def get_current_date_prefix(self):
        today = date.today()
        return today.strftime("%Y/%m/%d")


    def get_current_date_string(self):
        today = date.today()
        return today.strftime("%Y-%m-%d")


    def get_blob_prefix(self):
        return 'raw/' + self.get_current_date_prefix() + '/'


    def get_value(self, source: dict, field:str, out: dict):
        if field in source and source[field]['value'] != None:
            out[field] = source[field]['value']
        else:
            out[field] = ''


    def transform_internal(self, station_id: str, json_obj: dict) -> dict:
        # print(json_obj)

        data = {
            'stationId': station_id,
            'timestamp': json_obj['timestamp']
        }

        self.get_value(json_obj, 'temperature', data)
        self.get_value(json_obj, 'dewpoint', data)
        self.get_value(json_obj, 'windDirection', data)
        self.get_value(json_obj, 'windSpeed', data)
        self.get_value(json_obj, 'windGust', data)
        self.get_value(json_obj, 'barometricPressure', data)
        self.get_value(json_obj, 'seaLevelPressure', data)
        self.get_value(json_obj, 'visibility', data)
        self.get_value(json_obj, 'maxTemperatureLast24Hours', data)
        self.get_value(json_obj, 'minTemperatureLast24Hours', data)
        self.get_value(json_obj, 'precipitationLast3Hours', data)
        self.get_value(json_obj, 'relativeHumidity', data)
        self.get_value(json_obj, 'windChill', data)
        self.get_value(json_obj, 'heatIndex', data)

        return data


    def extract_station_id(self, station_str: str) -> str:
        return station_str.replace('https://api.weather.gov/stations/', '')


    def transform(self):
        print(f'Current date" {self.get_current_date_prefix()}')

        daily_csv_file_name = 'daily/' + self.get_current_date_prefix() + '/' + self.get_current_date_string() + '.csv'
        print(f'Daily file name: {daily_csv_file_name}')

        prefix = self.get_blob_prefix()

        transformed_list = []

        blobs = self.storage_client.list_blobs(self.bucket_name, prefix=prefix, delimiter='/')
        blob: Blob

        count=0

        for blob in blobs:
            count = count+1

            print(blob.name)
            json_obj = json.loads(blob.download_as_string())

            if 'properties' in json_obj:
                if 'station' in json_obj['properties']:
                    station_str =  json_obj['properties']['station']

                    station_id = self.extract_station_id(station_str)

                    transformed = self.transform_internal(station_id, json_obj['properties'])

                    if 'geometry' in json_obj:
                        transformed['latitude'] = json_obj['geometry']['coordinates'][1]
                        transformed['longitude'] = json_obj['geometry']['coordinates'][0]

                    # print(transformed)

                    transformed_list.append(transformed)

                    # df = pd.DataFrame([transformed])

                    # df = pd.DataFrame(transformed_list)
                    # self.save_to_staging(blob.name, df)

        print(f'total files processed: {count}')
        # print(transformed_list)

        df = pd.DataFrame(transformed_list)
        self.save_to_daily(daily_csv_file_name, df)


    def save_to_daily(self, filename:str, df: pd.DataFrame):
        blob = self.bucket.blob(filename)
        blob.upload_from_string(df.to_csv(index=False), 'text/csv')



    def save_to_staging(self, json_file:str, df: pd.DataFrame):
        csv_str = json_file.replace('.json', '.csv').replace('raw', 'staging')

        blob = self.bucket.blob(csv_str)
        blob.upload_from_string(df.to_csv(index=False), 'text/csv')



    def init(self):
        self.storage_client = self.create_storage_client()
        self.bucket = self.get_bucket()


def main():
    transformer=Transform()
    transformer.credentials_file='./google_credential.json'
    transformer.bucket_name='data-engineering-zoomcamp-2024-project'


    transformer.init()
    transformer.transform()


if __name__ == "__main__":
    main()
