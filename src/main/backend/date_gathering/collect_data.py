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
 
class CollectRawNBAData(TransformHelper):
 
    def __init__(self, **kwargs):
        self.season_year = kwargs['season_year']
        self.today = datetime.now().strftime('%Y-%m-%d')
 
    def get_games_played(self) -> pd.DataFrame:
        games = scoreboard.Scoreboard(day_offset=1, game_date=self.today)
        df_team_games_ids = games.get_data_frames()[0]

        return df_team_games_ids
 
    def get_players(self) -> pd.DataFrame:
        df_players = pd.DataFrame(players.get_active_players())
        df_players = df_players.loc[df_players['is_active'] == True]
        return df_players
 
    def get_team_roster(self, players_df) -> pd.DataFrame:
        team_id = list(set(players_df['TEAM_ID'].values.tolist()))
        self.transfrom_data(commonteamroster.CommonTeamRoster, team_id, )
        # all_teams = []
        # for id in team_id:
        #     team = commonteamroster.CommonTeamRoster(season=self.season_year, team_id=id)
        #     all_teams.append(team.get_data_frames()[0])
        df_team_roster = pd.concat(all_teams)[['TeamID', 'PLAYER_ID', 'PLAYER', 'AGE', 'POSITION']]

        return df_team_roster
    
    def get_team_info(self) -> pd.DataFrame:
        df_team_info = pd.DataFrame(teams.get_teams())

        return df_team_info
 
    def get_players_games_log(self, df_players: pd.DataFrame) -> pd.DataFrame:
        game_logs_arr = []
        player_ids = list(set(df_players['PLAYER_ID'].values.tolist()))

        for id in player_ids:
            t.sleep(1)
            player_game_log = playergamelog.PlayerGameLog(player_id=id)
            game_logs = player_game_log.get_data_frames()[0]
            game_logs_arr.append(game_logs)
        df_all_player_game_logs = pd.concat(game_logs_arr)

        return df_all_player_game_logs
 
    def get_team_logs(self, df_team_roster: pd.DataFrame) -> pd.DataFrame:
        team_game_logs_arr = []
        team_ids = list(set(df_team_roster['TeamID'].values.tolist()))

        for id in team_ids:
            t.sleep(1)
            team_game_log = teamgamelog.TeamGameLog(team_id=id, season=self.season_year)
            team_game_log = team_game_log.get_data_frames()[0]
            team_game_logs_arr.append(team_game_log)

        df_all_team_game_logs = pd.concat(team_game_logs_arr)

        return df_all_team_game_logs
 
    def gather_and_import_nba_data(self):
        df_team_info = self.get_team_info()

        return df_team_info
