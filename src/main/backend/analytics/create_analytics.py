
import pandas as pd
from datetime import datetime 
from utils.helper import StatHelper

class CreateAnalytics(StatHelper):
    def __init__(self, df_player_logs, df_player_info, df_game_logs, df_team_logs):
        self.df_player_logs = df_player_logs
        self.df_player_info = df_player_info
        self.df_game_logs = df_game_logs
        self.df_team_logs = df_team_logs

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=lambda col: col.lower())
    
    def overall_player_season_stats(self, df_player_logs: pd.DataFrame, df_player_info: pd.DataFrame) -> pd.DataFrame: 
        df_player_logs["game_date"] = df_player_logs['game_date'].apply(lambda x: datetime.strptime(x, "%b %d, %Y"))
        df_player_logs_joined = df_player_info.merge(df_player_logs, left_on="id", right_on="player_id")
        df_overall_player_stats = StatHelper.calculate_averages_all_columns(df_player_logs_joined, "full_name")
        
        return df_overall_player_stats

    def generate(self):
        df_player_logs, df_player_info, df_game_logs, df_team_logs = map(self.clean_dataframe, [self.df_player_logs, self.df_player_info, self.df_player_logs, self.df_team_logs])
        self.overall_player_season_stats(df_player_logs, df_player_info).to_csv("logs.csv")