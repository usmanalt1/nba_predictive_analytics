#!/usr/bin/env python3

from main.backend.utils.utils import DatabaseUtils

class CreateModelBasedOnSeason:
    def __init__(self, **kwargs):
        self.db = DatabaseUtils()
        self.year = kwargs["year"]
        self.team_standings = self.db.read_table("team_standings")
        self.player_stats = self.db.read_table("season_stats")
    
    def get_team_player_rankings(self, team_standings, player_stats):
        ranking = team_standings[["TeamID", "WINS", "LOSSES", "WinPCT"]].sort_values(by="WinPCT", ascending=False)
        ranking["TEAM_ID"] = ranking["TeamID"]
        ranking["ranking"] = ranking["WinPCT"].rank(ascending=False)
        ranking["ranking"] = ranking["ranking"].astype(int)
        merged_ranking_season_stats = player_stats.merge(ranking)

        return merged_ranking_season_stats
    
    # def prepare_data_for_model_fit(self, get_team_player_rankings):
        

