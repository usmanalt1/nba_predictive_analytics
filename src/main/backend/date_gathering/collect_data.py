from nba_api.stats.endpoints import scoreboard
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog, teamgamelog
from utils.utils import DatabaseUtils
import pandas as pd
from datetime import datetime
import time as t
from collections import namedtuple
from utils.transform_helper import TransformHelper 
import logging
 
class CollectRawNBAData(TransformHelper):
 
    def __init__(self, **kwargs):
        self.season_year = kwargs["season_year"]
        self.today = datetime.now().strftime("%Y-%m-%d")
 
    def get_games_played(self) -> pd.DataFrame:
        games = scoreboard.Scoreboard(day_offset=1, game_date=self.today)
        df_team_games_ids = games.get_data_frames()[0]

        return df_team_games_ids
    
    def get_team_info(self) -> pd.DataFrame:
        df_team_info = pd.DataFrame(teams.get_teams())

        logging.info("...Raw Team Info DF Generated")
        return df_team_info
 
    def get_team_roster(self, df_team_info: pd.DataFrame) -> pd.DataFrame:
        team_ids = df_team_info["id"].values.tolist()
        all_teams = self.transfrom_data(commonteamroster.CommonTeamRoster, team_ids, season=self.season_year)
        df_team_rosters = all_teams[["TeamID", "PLAYER_ID", "PLAYER", "AGE", "POSITION"]]

        logging.info("...Raw Team Roster DF Generated")
        return df_team_rosters
    
    def get_team_logs(self, df_team_roster: pd.DataFrame) -> pd.DataFrame:
        team_ids = df_team_roster['TeamID'].values.tolist()
        df_all_team_logs = self.transfrom_data(teamgamelog.TeamGameLog, team_ids, season=self.season_year)

        logging.info("...Raw Team Game Logs DF Generated")
        return df_all_team_logs
    
    def get_players(self) -> pd.DataFrame:
        df_players = pd.DataFrame(players.get_active_players())
        df_players = df_players.loc[df_players["is_active"] == True]

        logging.info("...Raw Player Info DF Generated")
        return df_players
 
    def get_players_games_log(self, df_players: pd.DataFrame) -> pd.DataFrame:
        player_ids = list(set(df_players["id"].values.tolist()))
        df_all_player_game_logs = self.transfrom_data(playergamelog.PlayerGameLog, player_ids)

        logging.info("...Raw Player Game Logs DF Generated")
        return df_all_player_game_logs
 
    def gather_and_import_nba_data(self):
        df_teams = self.get_team_info()
        df_teams_roster = self.get_team_roster(df_teams)
        df_team_game_logs = self.get_team_logs(df_teams_roster)
        
        df_players = self.get_players()
        df_plyer_game_logs = self.get_players_games_log(df_players)

        nba_data_dict = {
            "df_teams_info": df_teams,
            "df_teams_roster": df_teams_roster,
            "df_team_game_logs": df_team_game_logs,
            "df_players_info": df_players,
            "df_plyer_game_logs": df_plyer_game_logs
        }

        return nba_data_dict
