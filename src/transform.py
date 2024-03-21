import json
from google.cloud import storage
from datetime import datetime

class Transform:
    storage_client: storage.Client=None
    bucket_name:str=None
    bucket:storage.Bucket=None
    credentials_file:str=None


    def create_storage_client(self):
        return storage.Client.from_service_account_json(self.credentials_file)


    def get_bucket(self):
        return self.storage_client.bucket(self.bucket_name)


    def transform():
        print()



    def init(self):
        print()
    #     self.storage_client = self.create_storage_client()
    #     self.bucket = self.get_bucket()


def main():
    transformer=Transform()
    transformer.credentials_file='./google_credential.json'
    transformer.bucket_name='data-engineering-zoomcamp-2024-project'


    transformer.init()
    transformer.transform()


if __name__ == "__main__":
    main()