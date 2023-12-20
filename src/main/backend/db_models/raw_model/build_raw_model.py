from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

RawModel = declarative_base()

DEFAULT_SEASON_YEAR: str = "2023_24"

class TeamInfo(RawModel):
    __tablename__ = f"team_info_{DEFAULT_SEASON_YEAR}"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    abbreviation = Column(String)
    nickname = Column(String)
    city = Column(String)
    state = Column(String)
    year_founded = Column(Integer)

class TeamLogsStats(RawModel):
    __tablename__ = f"team_logs_{DEFAULT_SEASON_YEAR}"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("team_info.id"))
    game_id = Column(String)
    game_date = Column(Date)
    matchup = Column(String)
    wl = Column(String)
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

    team_logs = relationship("TeamInfo", backref=f"team_logs_{DEFAULT_SEASON_YEAR}")

class PlayerInfo(RawModel):
    __tablename__ = "player_info"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean)


class PlayerLogsStats(RawModel):
    __tablename__ = "player_logs"

    id = Column(Integer, primary_key=True)  
    player_id = Column(Integer, ForeignKey("player_info.id"))
    season_id = Column(Integer)
    game_id = Column(String)
    game_date = Column(Date)
    matchup = Column(String)
    wl = Column(String)
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

    player_logs = relationship("PlayerInfo", backref="player_logs_{DEFAULT_SEASON_YEAR}")


