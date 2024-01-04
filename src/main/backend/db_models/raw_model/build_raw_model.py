from sqlalchemy import Column, Integer, String, Boolean, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_models.registry import Registry_new


RawModel = declarative_base()

class SeasonInfo(RawModel): 
    __tablename__ = f"season_info"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer)

class TeamInfo(RawModel):
    __tablename__ = f"team_info"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer)
    full_name = Column(String(255))
    abbreviation = Column(String(255))
    nickname = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    year_founded = Column(Integer)

class TeamLogsStats(RawModel):
    __tablename__ = f"team_logs"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    season_id = Column(Integer)
    game_id = Column(String(255))
    game_date = Column(Date)
    matchup = Column(String(255))
    wl = Column(String(255))
    w = Column(Integer)
    l = Column(Integer)
    w_pct = Column(Float)
    min = Column(Integer)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    tov = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)

class PlayerInfo(RawModel):
    __tablename__ = "player_info"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer)
    full_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_active = Column(Boolean)

class PlayerLogsStats(RawModel):
    __tablename__ = "player_logs"

    id = Column(Integer, primary_key=True)  
    player_id = Column(Integer)
    season_id = Column(Integer)
    game_id = Column(String(255))
    game_date = Column(Date)
    matchup = Column(String(255))
    wl = Column(String(255))
    min = Column(Integer)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    tov = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Integer)
    video_available = Column(Boolean)


class TeamRoster(RawModel):
    __tablename__ = f"team_roster"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    player = Column(String(255))
    age = Column(Integer)
    player_id = Column(Integer)
    season_id = Column(Integer)


