#!/usr/bin/env python3

import nba_api
from nba_api.stats.endpoints import boxscoreplayertrackv2
from nba_api.stats.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats, leaguestandings, teamyearbyyearstats
from nba_api.stats.static import players
import multiprocessing
from argparse import ArgumentParser
from datetime import datetime, timedelta
import json
import sqlite3 as sq
import pandas as pd
import time as t
from main.backend.utils.utils import DatabaseUtils

class ExtractAndSaveNbaData(DatabaseUtils):
    def __init__(self, year):
        self.year = '2023-24'
        self.today = datetime.now().strftime('%Y-%m-%d')
        # self.yesterday = self.today - timedelta(days=1)
        # self.formatted_yesterday = self.yesterday.strftime('%Y-%m-%d')
  
    def get_players(self):
        players = commonallplayers.CommonAllPlayers(season = self.year)
        players_json = players.get_json()
        players = json.loads(players_json)
        headers = players['resultSets'][0]['headers']
        rows = players['resultSets'][0]['rowSet']
        headers = list(map(str.lower,headers))
        construct_json = []
        for row in rows:
            construct_json.append(dict(zip(headers, row)))
        df = pd.DataFrame.from_dict(construct_json) 
        df['from_year'] = df['from_year'].astype(float)
        df = df.loc[(df['from_year'] == 2022)]
        self.save_in_df(df, "players_2324")
        print("Player DF saved")
        return df

    def get_team_roster(self, players_df):
        team_id = list(set(players_df.team_id.values.tolist()))

        all_teams = []
        clean_list = ["TeamID","PLAYER_ID", "PLAYER", "AGE", "POSITION"]
        for id in team_id:
            team_json = commonteamroster.CommonTeamRoster(season = self.year, team_id = id).get_json()
            headers = json.loads(team_json)['resultSets'][0]['headers']
            rows = json.loads(team_json)['resultSets'][0]['rowSet']
            for row in rows:
                headers_to_rows = dict(zip(headers, row))
                clean_dict = {}
                for k, v in headers_to_rows.items():
                    if k in clean_list:
                        clean_dict[k] = v
                all_teams.append(clean_dict)
        df = pd.DataFrame.from_dict(all_teams)
        self.save_in_df(df, "team_roster_2324")
        print("Team Roster saved")
        return df


    def get_player_logs(self):
        construct_json = []
        game_logs = playergamelogs.PlayerGameLogs(season_nullable="2022-23").get_json()
        rows = json.loads(game_logs)['resultSets'][0]['rowSet']
        headers = json.loads(game_logs)['resultSets'][0]['headers']

        for row in rows:
            construct_json.append(dict(zip(headers, row)))

        df = pd.DataFrame.from_dict(construct_json)
        print("Player logs saved")
        self.save_in_df(df, "player_logs")
        return df

    def get_season_stats(self,team_df, year, to_year):
        players_id = team_df["PLAYER_ID"].values.tolist()
        construct_json = []
        
        for id in players_id:
            try: 
                game_logs = playercareerstats.PlayerCareerStats(per_mode36="PerGame", player_id=id, timeout=10).get_json()
                rows = json.loads(game_logs)['resultSets'][0]['rowSet']
                headers = json.loads(game_logs)['resultSets'][0]['headers']

                for row in rows:
                    if f"{year}-{to_year}" in row:
                        headers_to_rows = dict(zip(headers, row))
                        construct_json.append(headers_to_rows)
                        print(headers_to_rows)
            except:
                print("DO NOTHING")
        
        df = pd.DataFrame.from_dict(construct_json)
        self.db.save_in_df(df, "season_stats")
        print("Season Stats saved")
        return df
    
    def team_standings(self, season_year):
        team_ranking = leaguestandings.LeagueStandings(league_id="00", season=season_year, season_type="Regular Season").get_json()
        rows = json.loads(team_ranking)['resultSets'][0]['rowSet']
        headers = json.loads(team_ranking)['resultSets'][0]['headers']
        construct_json = []
        for row in rows:
            construct_json.append(dict(zip(headers, row)))
        df = pd.DataFrame.from_dict(construct_json) 
        self.save_in_df(df, "team_standings")
        return df

    def team_stats(self, team):
        team_ranking = teamyearbyyearstats.TeamYearByYearStats(league_id="00", per_mode_simple="PerGame", season_type_all_star="Regular Season", team_id=team).get_json() 
    
    
    def get_game_specific_scoreboard(self, team_roster_df):
        games = scoreboard.Scoreboard(day_offset=1, game_date=self.today)
        team_games_ids = games.get_data_frames()[0][["GAME_ID", "HOME_TEAM_ID", "VISITOR_TEAM_ID"]]
        get_teams_players = team_roster_df[(team_roster_df["TeamID"].isin(team_games_ids["HOME_TEAM_ID"])) | (team_roster_df["TeamID"].isin(team_games_ids["VISITOR_TEAM_ID"]))]
        merge_game_ids = get_teams_players.merge(team_games_ids, left_on="TeamID", right_on="HOME_TEAM_ID")
        game_ids = team_games_ids["GAME_ID"].values.tolist()
        game_logs_arr = []
        for id in game_ids:
            player_ids = merge_game_ids.loc[merge_game_ids["GAME_ID"] == id].person_id.values.tolist()
            for id in player_ids:
                player_game_log = playergamelog.PlayerGameLog(player_id=id)
                game_logs = player_game_log.get_data_frames()[0]
                game_logs_arr.append(game_logs)
                
        df_all_player_game_logs = pd.concat(game_logs_arr)
        self.save_in_df(df_all_player_game_logs, "all_player_logs")


    def get_players_scoreboard(self, players):
        # games = scoreboard.Scoreboard(day_offset=1, game_date=self.today)
        # team_games_ids = games.get_data_frames()[0][["GAME_ID", "HOME_TEAM_ID", "VISITOR_TEAM_ID"]]
        # get_teams_players = team_roster_df[(team_roster_df["TeamID"].isin(team_games_ids["HOME_TEAM_ID"])) | (team_roster_df["TeamID"].isin(team_games_ids["VISITOR_TEAM_ID"]))]
        # merge_game_ids = get_teams_players.merge(team_games_ids, left_on="TeamID", right_on="HOME_TEAM_ID")
        # game_ids = team_games_ids["GAME_ID"].values.tolist()
        game_logs_arr = []

        # for id in game_ids:
        player_ids = players.person_id.values.tolist()
        for id in player_ids:
            t.sleep(1)
            player_game_log = playergamelog.PlayerGameLog(player_id=id, date_from_nullable=self.today)
            game_logs = player_game_log.get_data_frames()[0]
            game_logs_arr.append(game_logs)
        
        df_all_player_game_logs = pd.concat(game_logs_arr)
        self.save_in_df(df_all_player_game_logs, "all_player_logs")
        
        return df_all_player_game_logs


    def create_dfs(self):
        # self.db.create_db()
        players_df = self.get_players()
        team = self.get_team_roster(players_df)
        # team = self.db.read_table("team_roster_2324")
        # print(team)
        # self.get_players_scoreboard(players_df)

        # player_logs = self.get_season_stats(team, self.year, "23")
        # team_standings = self.team_standings(f"{self.year}-23")
