import pandas as pd

class StatHelper:
    def calculate_averages_all_columns(self, df: pd.DataFrame, grouped_col: str) -> pd.DataFrame:
        stat_columns = df.select_dtypes(include=['number']).columns
        df = df.groupby(grouped_col)[stat_columns].mean()

        return df
    
    def calculate_cumlative_sums(df: pd.DataFrame, group_by_columns: [str, str], assign_df_column_name: str, df_column_name: str) -> pd.DataFrame:
        df[assign_df_column_name] = df.groupby(group_by_columns)[df_column_name].cumsum()

    def logs_cumlative(self, df) -> pd.DataFrame:
        grouped_cols = ["full_name", "game_date"]
        df.sort_values(by=grouped_cols, inplace=True) 
    
        df_pts = self.calculate_cumlative_sums(df, grouped_cols, "pts_cumlative_sum", "pts")
        df_rebs = self.calculate_cumlative_sums(df_pts, grouped_cols, "rebs_cumlative_sum", "reb")
        df_asts = self.calculate_cumlative_sums(df_rebs, grouped_cols, "asts_cumlative_sum", "ast")
        df_fgpct = self.calculate_cumlative_sums(df_asts, grouped_cols, "fgpct_cumlative_sum", "fg_pct")
        df_fgpct3 = self.calculate_cumlative_sums(df_fgpct, grouped_cols, "fgpct3_cumlative_sum", "fg3_pct")
        # df_player_logs_cum_sum_plus_minus = self.calculate_cumlative_sums(df_player_logs_cum_sum_fgpct3, grouped_cols, "+-_cumlative_sum", "plus_mnus")

        return df_fgpct3