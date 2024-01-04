import json
import sqlite3 as sq
import pandas as pd
import time as t
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy


class DatabaseUtils:
    def __init__(self, db_url):
        self.db_url= db_url
        self.connection = create_engine(self.db_url, echo=True)
    
    def create_db(self):
        if not database_exists(self.db_url):
            create_database(self.db_url)

    def save_in_db_if_not_exists(self, df, table_name):
        if not sqlalchemy.inspect(self.connection).has_table(table_name):
            df.to_sql(table_name, con = self.connection, if_exists='replace', index=False) # writes to file
        else:
            self.read_table(table_name)
    
    def check_in_db(self, table_name):
        if sqlalchemy.inspect(self.connection).has_table(table_name):
            return True
    
    def read_table(self, table_name):
        df = pd.read_sql_table(table_name, self.connection)
        return df
    
    def save_in_db_if_exists(self, df, table_name):
        df.to_sql(table_name, con = self.connection, if_exists='replace', index=False)


