import requests
import traceback
import logging
import json
from google.cloud import storage
from datetime import datetime


class WeatherDataLoader:

    storage_client: storage.Client=None
    bucket_name:str=None
    bucket:storage.Bucket=None
    credentials_file:str=None
    station_list_file:str
    station_ids:list=None

    # offic_ids = [
    #     'AKQ','ALY','BGM','BOX','BTV','BUF','CAE','CAR','CHS','CLE','CTP','GSP',
    #     'GYX','ILM','ILN','LWX','MHX','OKX','PBZ','PHI','RAH','RLX','RNK','ABQ',
    #     'AMA','BMX','BRO','CRP','EPZ','EWX','FFC','FWD','HGX','HUN','JAN','JAX',
    #     'KEY','LCH','LIX','LUB','LZK','MAF','MEG','MFL','MLB','MOB','MRX','OHX',
    #     'OUN','SHV','SJT','SJU','TAE','TBW','TSA','ABR','APX','ARX','BIS','BOU',
    #     'CYS','DDC','DLH','DMX','DTX','DVN','EAX','FGF','FSD','GID','GJT','GLD',
    #     'GRB','GRR','ICT','ILX','IND','IWX','JKL','LBF','LMK','LOT','LSX','MKX',
    #     'MPX','MQT','OAX','PAH','PUB','RIW','SGF','TOP','UNR','BOI','BYZ','EKA',
    #     'FGZ','GGW','HNX','LKN','LOX','MFR','MSO','MTR','OTX','PDT','PIH','PQR',
    #     'PSR','REV','SEW','SGX','SLC','STO','TFX','TWC','VEF','AER','AFC','AFG',
    #     'AJK','ALU','GUM','HPA','HFO','PPG','STU','NH1','NH2','ONA','ONP'
    # ]

    offic_ids = [
        'AKQ','ALY','BGM','BOX','BTV','BUF','CAE','CAR','CHS','CLE','CTP','GSP',
        'GYX','ILM','ILN','LWX','MHX','OKX','PBZ','PHI','RAH','RLX','RNK','ABQ',
        'AMA','BMX','BRO','CRP','EPZ','EWX','FFC','FWD','HGX','HUN','JAN','JAX',
        'KEY','LCH','LIX','LUB','LZK','MAF','MEG','MFL','MLB','MOB','MRX','OHX'
    ]

    def create_storage_client(self):
        return storage.Client.from_service_account_json(self.credentials_file)


    def get_bucket(self):
        return self.storage_client.bucket(self.bucket_name)


    def upload_to_bucket(self, content: str, blob_name: str):
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(content)


    def tick(self):
        # for each office, first we retrieve a list of approved observation stations.
        for office_id in self.offic_ids:

            # office specific url
            url = 'https://api.weather.gov/offices/' + office_id

            # send request
            response = requests.get(url)

            # get the response in dict
            response_json: dict = response.json()

            if 'approvedObservationStations' in response_json:
                approvedObservationStations = response_json['approvedObservationStations']

                for approvedObservationStation in approvedObservationStations:
                    # extract station id and then retrieve latest data
                    station_id = approvedObservationStation.replace('https://api.weather.gov/stations/','')

                    # station specific url
                    url = 'https://api.weather.gov/stations/' + station_id + '/observations/latest'

                    print(f'Calling {url}')

                    response_json: dict = None

                    try:
                        # send request
                        response = requests.get(url)

                        if response is None:
                            print('response is None, skipping')
                            continue

                        # get the response in dict
                        response_json = response.json()
                    except Exception as e:
                        print(f'Error retrieving data, url: {url}')
                        logging.error(traceback.format_exc())
                        continue

                    if response_json is None:
                        print('response_json is None, skipping')
                        continue

                    # we like to extract timestamp field which is in properties.timestamp field
                    if 'properties' in response_json:
                        properties = response_json['properties']

                        if 'timestamp' in properties:
                            timestamp_string = properties['timestamp']

                            # based on the timestamp, determine the blob name
                            blob_name = self.generate_blob_name(office_id, station_id, timestamp_string)
                            print(f'offic_id {office_id}, station_id {station_id}, timestamp is {timestamp_string}, blob name is {blob_name}')

                            # convert from dict to string as storage client can process string without
                            # us having to store it to local file then upload.
                            content:str = json.dumps(response_json)

                            # Upload the file to the bucket
                            self.upload_to_bucket(content, blob_name)
                        else:
                            print(f'offic_id {office_id}, station_id {station_id}, no timestamp field found in the response')
                    else:
                        print(f'offic_id {office_id}, station_id {station_id}, no properties field found in the response')


    def generate_blob_name(self, office_id, station_id: str, timestamp_string: str):
        # example: 2024-03-21T11:07:00+00:00
        timestamp = datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S%z')
        # print(type(timestamp))

        # construct blob name in GCS
        blob_name = 'raw/{year}/{month}/{day}/{hour}_{minute}_{office_id}_{station_id}.json'.format(
            year=timestamp.year,
            month=str(timestamp.month).zfill(2),
            day=str(timestamp.day).zfill(2),
            hour=str(timestamp.hour).zfill(2),
            minute=str(timestamp.minute).zfill(2),
            office_id=office_id,
            station_id=station_id
            )

        return blob_name



    def init(self):
        self.station_ids = self.read_station_list()
        self.storage_client = self.create_storage_client()
        self.bucket = self.get_bucket()


    def read_station_list(self):
        with open(self.station_list_file) as file:
            return [line.rstrip() for line in file]



def main():
    loader=WeatherDataLoader()
    loader.credentials_file='./google_credential.json'
    loader.bucket_name='data-engineering-zoomcamp-2024-project'
    loader.station_list_file='src/station_list.txt'

    loader.init()
    loader.tick()



if __name__ == "__main__":
    main()

