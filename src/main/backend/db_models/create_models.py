from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from utils.utils import DatabaseUtils
from db_models.raw_model.build_raw_model import RawModel


class CreateModels(DatabaseUtils):
    def __init__(self, db_url, year):
        super().__init__(db_url)
    
    def create_db_models(self):
        self.create_db()
        return 

    def create(self):
        # DEFAULT_SEASON_YEAR = Registry_new.get("default_season_year")
        # print(DEFAULT_SEASON_YEAR)
        Base = RawModel
        Base.metadata.create_all(self.connection)
    

    