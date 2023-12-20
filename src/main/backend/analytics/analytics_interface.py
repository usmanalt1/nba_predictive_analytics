from abc import ABC, abstractmethod
import pandas as pd

class AnalyticsInterface(ABC):
    @abstractmethod
    def overall_player_season_stats(self) -> pd.DataFrame: 
        pass

    @abstractmethod
    def overall_team_season_stats(self)-> pd.DataFrame:
        pass
