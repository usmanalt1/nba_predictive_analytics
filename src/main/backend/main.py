#!/usr/bin/env python3

from date_gathering.collect_data import CollectRawNBAData
from utils.utils import DatabaseUtils 
from analytics.create_analytics import CreateAnalytics
import pandas as pd
from db_models.create_models import CreateModels

def main() -> pd.DataFrame:
    # ExtractAndSaveNbaData("2022").create_dfs()
    # CreateModelBasedOnSeason(year="2022").get_team_rankings()
    # db = DatabaseUtils()
    # CollectRawNBAData(season_year="2023-24").gather_and_import_nba_data()
    # df_games_played = db.read_table("games_played_2324")
    # df_players_info = db.read_table("players_2324")
    # df_team_roster = db.read_table("team_roster_2324")
    # df_player_game_logs = db.read_table("player_game_logs_2324")
    # df_team_game_logs = db.read_table("team_game_logs_2324")
    # df_team_game_logs = db.read_table("team_info_2324")

    # CreateAnalytics(df_player_game_logs, df_players_info, df_games_played, df_team_game_logs, df_team_game_logs).generate()
    CreateModels.create()

    

if __name__ == "__main__":
    main()