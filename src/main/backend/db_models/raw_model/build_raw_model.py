from sqlalchemy import Column, Integer, String, Boolean, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_models.registry import Registry_new


RawModel = declarative_base()

class SeasonInfo(RawModel): 
    __tablename__ = f"season_info"

    id = Column(Integer, primary_key=True)
    season_year = Column(Integer)

class TeamInfo(RawModel):
    __tablename__ = f"team_info"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey(f"season_info.id"))
    full_name = Column(String(255))
    abbreviation = Column(String(255))
    nickname = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    year_founded = Column(Integer)

    team_info = relationship("SeasonInfo", backref=f"team_info")

class TeamLogsStats(RawModel):
    __tablename__ = f"team_logs"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey(f"team_info.id"))
    season_id = Column(Integer, ForeignKey(f"season_info.id"))
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

    team_logs = relationship("TeamInfo", backref=f"team_logs")
    season_info = relationship("SeasonInfo", backref=f"team_logs")

class PlayerInfo(RawModel):
    __tablename__ = "player_info"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey(f"season_info.id"))
    full_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_active = Column(Boolean)

    season_info = relationship("SeasonInfo", backref=f"player_info")

class PlayerLogsStats(RawModel):
    __tablename__ = "player_logs"

    id = Column(Integer, primary_key=True)  
    player_id = Column(Integer, ForeignKey("player_info.id"))
    season_id = Column(Integer, ForeignKey(f"season_info.id"))
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

    player_logs = relationship("PlayerInfo", backref="player_logs")
    season_info = relationship("SeasonInfo", backref=f"player_logs")

