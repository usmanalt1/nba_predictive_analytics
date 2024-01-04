#!/usr/bin/env python3

from date_gathering.collect_data import CollectRawNBAData
from utils.utils import DatabaseUtils
from utils.s3_helper import S3Helper
from analytics.create_analytics import CreateAnalytics
import pandas as pd
from db_models.create_models import CreateModels
import logging
from datetime import datetime, timedelta
import argparse

logging.basicConfig(level=logging.INFO)
DB_URL = "mysql+pymysql://root:""@127.0.0.1:3306/nba_test"

def main() -> pd.DataFrame:
    date = (datetime.today() - timedelta(days=1))
    parser = argparse.ArgumentParser(description="Check if an S3 bucket exists.")
    parser.add_argument("--date", default=date,
                    help='Date in the format YYYY-MM-DD (default: today\'s date)')
    
    args = parser.parse_args()
    raw_tables = CollectRawNBAData(date_to_run=args.date).gather_and_import_nba_data()

    init_s3 = S3Helper(args.date)
    init_s3.save_tables_from_dict(raw_tables, "nba-analytics-ma")

    init_models = CreateModels(DB_URL, args.date)
    getattr(init_models, "create")()
    getattr(init_models, "insert")(raw_tables)
    
   
    # build_analytics = CreateAnalytics()
    save_analytics_table = ""
    

if __name__ == "__main__":
    main()