from raw_model.build_raw_model import RawModel
from sqlalchemy import create_engine
 
class CreateModels:
    def __init__(self, year):
        self.year = year
        self.db_url="mysql+pymysql://root:""@127.0.0.1:3306/nba_test"
        self.connection = create_engine(self.db_url, echo=True)

    def get_season(self):
        return ""
    

    def create(self):
        Base = RawModel 
        Base.metadata.create_all(self.connection)
        
