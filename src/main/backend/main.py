#!/usr/bin/env python3

from date_gathering.collect_data import CollectRawNBAData
from utils.utils import DatabaseUtils 
from analytics.create_analytics import CreateAnalytics
import pandas as pd
from db_models.create_models import CreateModels

def main() -> pd.DataFrame:
    get_raw_tables = ""
    save_raw_table_s3 = ""
    build_raw_model = ""
    save_raw_tables = ""
    build_analytics = ""
    save_analytics_table = ""

    # CreateAnalytics(df_player_game_logs, df_players_info, df_games_played, df_team_game_logs, df_team_game_logs).generate()
    created = CreateModels("mysql+pymysql://root:""@127.0.0.1:3306/nba_test", "2014")
    created.create()

if __name__ == "__main__":
    main()