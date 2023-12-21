
import pandas as pd
from datetime import datetime 
from utils.stat_helper import StatHelper

class CreateAnalytics(StatHelper):
    def __init__(self, df_player_logs, df_player_info, df_game_logs, df_team_logs, df_team_info):
        self.df_player_logs = df_player_logs
        self.df_player_info = df_player_info
        self.df_game_logs = df_game_logs
        self.df_team_logs = df_team_logs
        self.df_team_info = df_team_info

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns=lambda col: col.lower())
        df["game_date"] = self.df['game_date'].apply(lambda x: datetime.strptime(x, "%b %d, %Y"))
        return df
    
    def clean_player_log_stats(self) -> pd.DataFrame:
        self.df_player_logs = self.clean_dataframe(self.df_player_logs)
        df_player_logs_joined = self.df_player_info.merge(self.df_player_logs, left_on="id", right_on="player_id")

        return df_player_logs_joined
    
    def clean_team_log_stats(self) -> pd.DataFrame:
        self.df_game_logs = self.clean_dataframe(self.df_game_logs)
        df_team_logs_joined = self.df_team_logs.merge(self.df_team_info, on="team_id")

        return df_team_logs_joined
    
    def overall_player_season_stats(self, df_clean_player_log_stats) -> pd.DataFrame: 
        df_overall_player_stats = self.calculate_averages_all_columns(df_clean_player_log_stats, "full_name")
        return df_overall_player_stats

    def overall_team_season_stats(self, df_clean_team_log_stats) -> pd.DataFrame:
        df_overall_team_stats = self.calculate_averages_all_columns(df_clean_team_log_stats, "full_name")
        return df_overall_team_stats
    
    def player_logs_cumlative(self, df_clean_player_log_stats) -> pd.DataFrame:
        df_player_logs_cum_sum = self.logs_cumlative(df_clean_player_log_stats)
        df_player_logs_cum_sum_plus_minus = self.calculate_cumlative_sums(df_player_logs_cum_sum, ["full_name", "game_date"], "+-_cumlative_sum", "plus_mnus")

        return df_player_logs_cum_sum_plus_minus
    
    def team_logs_cumlative(self, df_clean_team_log_stats) -> pd.DataFrame:
        df_team_logs_cum_sum = self.logs_cumlative(df_clean_team_log_stats)

        return df_team_logs_cum_sum

    def build_analytics(self):
        player_logs = self.clean_player_log_stats()
        team_logs = self.clean_team_log_stats()
        player_stats = self.overall_player_season_stats(player_logs)
        team_stats = self.overall_team_season_stats(team_logs)
        player_cum_sum = self.player_logs_cumlative(player_logs)
        team_cum_sum = self.team_logs_cumlative(team_logs)

        analytics_dict = {
            "player_logs": player_logs,
            "team_logs": team_logs,
            "player_stats": player_stats,
            "team_stats": team_stats,
            "player_cum_sum": player_cum_sum,
            "team_cum_sum": team_cum_sum
        }
        return analytics_dict