import boto3
import logging
import pandas as pd
from utils.transform_helper import TransformHelper

# AWS credentials and region
AWS_ACCESS_KEY_ID = "AKIAYBX4X3NVTURDJARR"
AWS_SECRET_ACCESS_KEY = "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"
REGION_NAME = "eu-west-2"


class S3Helper(TransformHelper):

    def __init__(self, date):
        self.date = date
        self.s3 = boto3.client("s3", 
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=REGION_NAME)

    def create_bucket(self, bucket_name: str):

        try: 
            self.s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': REGION_NAME  # Specify the region for the bucket
            }
        )
            logging.info(f"Bucket: {bucket_name} created")
        except Exception as e:
            logging.info(f"Exception: {e} when creating bucket: {bucket_name}")

        
    def save_in_bucket(self, df: pd.DataFrame, bucket_name: str, date: str, table_name: str, season_year: str):
        file_path = f"{season_year}/{date}/{table_name}"
        self.create_bucket(bucket_name)

        try: 
            df.to_csv(f"s3://{bucket_name}/{file_path}/{table_name}.csv")
            logging.info(f"csv saved: s3://{bucket_name}/{file_path}/{table_name}.csv")
        except Exception as e:
            logging.info(f"Exception: {e} when uploading csv: {bucket_name}/{file_path}")
    
    def save_tables_from_dict(self, dict, bucket_name):
        formatted_date = self.date.strftime("%Y-%m-%d")
        season_year = self.create_season_id_year().get("season_year")
        for k, v in dict.items():
            self.save_in_bucket(v, bucket_name, formatted_date, k, season_year)







    

        
