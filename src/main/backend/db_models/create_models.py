from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from utils.utils import DatabaseUtils
from utils.transform_helper import TransformHelper
from db_models.raw_model.build_raw_model import RawModel, SeasonInfo, TeamInfo, TeamLogsStats, PlayerInfo, PlayerLogsStats, TeamRoster
from sqlalchemy.orm import sessionmaker
import logging
import datetime

class CreateModels(DatabaseUtils, TransformHelper):
    def __init__(self, db_url, date):
        super().__init__(db_url)
        self.Session = sessionmaker(bind=self.connection)
        self.session = self.Session()
        self.date = date
    
    def create_db_models(self):
        self.create_db()

    def create(self):
        Base = RawModel
        Base.metadata.create_all(self.connection)

    def overwrite(self, dict_dfs, df_name, model):

        id = int(self.create_season_id_year().get("season_id"))
        query_for_season_year_count = self.session.query(SeasonInfo).filter_by(season_id=id).count()

        if df_name == "df_season_record" and query_for_season_year_count > 0:
            logging.info("Nothing to overwrite in df_season_record")
        elif df_name == "df_season_record" and  query_for_season_year_count == 0:
            df = dict_dfs.get("df_season_record").to_dict(orient="records")
            self.session.bulk_insert_mappings(SeasonInfo, df)
            logging.info("Adding new season to table")
        else:
            df = dict_dfs.get(df_name).to_dict(orient="records")
            season_id = self.session.query(SeasonInfo).filter_by(season_id=id).first().season_id
            delete_statement = model.__table__.delete().where(model.season_id == season_id)
            self.session.execute(delete_statement)
            self.session.bulk_insert_mappings(model, df)

            logging.info(f"Overritten table {model.__table__}")

    # def upsert(self, dict_dfs, df_name, model):
    #     formatted_date = self.date.strftime("%Y-%m-%d")
    #     date = datetime.strptime(formatted_date, "%Y-%m-%d")
    #     check_for_game_date = self.session.query(model).filter_by(game_date=date).count()
    #     df = dict_dfs.get(df_name).to_dict(orient="records")

    #     if check_for_game_date == 0: 
    #         self.session.bulk_insert_mappings(model, df)
    #         logging.info(f"Adding new data in {model.__table__}")
    #     else:
    #         delete_statement = model.__table__.delete().where(model.game_date == date)
    #         self.session.execute(delete_statement)
    #         self.session.bulk_insert_mappings(model, df)

    #         logging.info(f"Overritten table {model.__table__}")


    def insert(self, dict_dfs):
        ## static_tables
        self.overwrite(dict_dfs, "df_season_record", SeasonInfo)
        self.overwrite(dict_dfs, "df_teams_info", TeamInfo)
        self.overwrite(dict_dfs, "df_players_info", PlayerInfo)
        self.overwrite(dict_dfs, "df_teams_roster", TeamRoster)
        self.overwrite(dict_dfs, "df_team_game_logs", TeamLogsStats)


        self.session.commit()
        self.session.close()


    

    