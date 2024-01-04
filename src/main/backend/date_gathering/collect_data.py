from nba_api.stats.endpoints import scoreboard
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog, teamgamelog, leaguestandings
from utils.utils import DatabaseUtils
import pandas as pd
from datetime import datetime
import time as t
from collections import namedtuple
from utils.transform_helper import TransformHelper 
import logging
 
class CollectRawNBAData(TransformHelper):
 
    def __init__(self, **kwargs):
        self.date = kwargs["date_to_run"]
        self.season_id = self.create_season_id_year().get("season_id")
        self.season_year =  self.create_season_id_year().get("season_year")

    def get_season_year(self) -> pd.DataFrame:

        season_year_dict = {"season_id": [int(self.season_id)]}
        df_from_dict = pd.DataFrame.from_dict(season_year_dict)

        logging.info("...Raw Season Info DF Generated")
        return df_from_dict

    def get_games_played(self) -> pd.DataFrame:
        games = scoreboard.Scoreboard(day_offset=1, game_date=self.today)
        df_team_games_ids = games.get_data_frames()[0]

        return df_team_games_ids
    
    def get_team_info(self) -> pd.DataFrame:
        df_team_info = pd.DataFrame(teams.get_teams())
        df_team_info = self.clean_dataframe(df_team_info)
        df_team_info["season_id"] = int(self.season_id)

        logging.info("...Raw Team Info DF Generated")
        return df_team_info
 
    def get_team_roster(self, df_team_info: pd.DataFrame) -> pd.DataFrame:
        team_ids = df_team_info["id"].values.tolist()
        all_teams = self.transfrom_data(commonteamroster.CommonTeamRoster, team_ids, season=self.season_year)
        all_teams = self.clean_dataframe(all_teams)
        all_teams["team_id"] = all_teams["teamid"] 
        df_team_rosters = all_teams[["team_id", "player_id", "player", "age", "position"]]
        df_team_rosters["season_id"] = int(self.season_id)

        logging.info("...Raw Team Roster DF Generated")
        return df_team_rosters
    
    def get_team_logs(self, df_team_roster: pd.DataFrame) -> pd.DataFrame:
        team_ids = df_team_roster["team_id"].values.tolist()
        df_all_team_logs = self.transfrom_data(teamgamelog.TeamGameLog, team_ids, season=self.season_year)
        df_all_team_logs = self.clean_dataframe(df_all_team_logs)
        df_all_team_logs["teamid"] = df_all_team_logs["team_id"]
        df_all_team_logs["game_date"] = df_all_team_logs["game_date"].apply(self.convert_date_format)
        df_all_team_logs["season_id"] = int(self.season_id)

        logging.info("...Raw Team Game Logs DF Generated")
        return df_all_team_logs
    
    def get_players(self) -> pd.DataFrame:
        df_players = pd.DataFrame(players.get_active_players())
        df_players = df_players.loc[df_players["is_active"] == True]
        df_players["season_id"] = int(self.season_id)

        logging.info("...Raw Player Info DF Generated")
        return df_players
 
    def get_players_games_log(self, df_players: pd.DataFrame) -> pd.DataFrame:
        player_ids = list(set(df_players["id"].values.tolist()))
        df_all_player_game_logs = self.transfrom_data(playergamelog.PlayerGameLog, player_ids)
        df_all_player_game_logs = self.clean_dataframe(df_all_player_game_logs)
        df_all_player_game_logs["game_date"] = df_all_player_game_logs["game_date"].apply(self.convert_date_format)

        logging.info("...Raw Player Game Logs DF Generated")
        return df_all_player_game_logs
 
    def gather_and_import_nba_data(self):
        df_season = self.get_season_year()
        df_teams = self.get_team_info()
        df_players = self.get_players()
        df_teams_roster = self.get_team_roster(df_teams)
        df_team_game_logs = self.get_team_logs(df_teams_roster)
        
        # df_plyer_game_logs = self.get_players_games_log(df_players)

        nba_data_dict = {
            "df_season_record": df_season,
            "df_teams_info": df_teams,
            "df_teams_roster": df_teams_roster,
            "df_team_game_logs": df_team_game_logs,
            "df_players_info": df_players
            # "df_plyer_game_logs": df_plyer_game_logs
        }

        return nba_data_dict
