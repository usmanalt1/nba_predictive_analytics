import pandas as pd

class StatHelper:
    def calculate_averages_all_columns(df: pd.DataFrame, grouped_col: str) -> pd.DataFrame:
        stat_columns = df.select_dtypes(include=['number']).columns
        df = df.groupby(grouped_col)[stat_columns].mean()

        return df