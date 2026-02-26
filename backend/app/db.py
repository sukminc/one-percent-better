from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///./action_tracker.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()


class Hand(Base):
    __tablename__ = "hands"

    id = Column(Integer, primary_key=True, index=True)
    game_no = Column(String, unique=True, index=True)
    table_name = Column(String)
    game_type = Column(String)
    stakes = Column(String)
    
    # Hero Cards & Position
    hero_cards = Column(String)
    hero_position = Column(String)
    hero_result = Column(Integer)
    
    # Pre-Flop Stats
    hero_vpip = Column(Boolean, default=False)
    hero_pfr = Column(Boolean, default=False)
    hero_three_bet = Column(Boolean, default=False)
    hero_fold_to_three_bet = Column(Boolean, default=False)
    
    # Post-Flop Stats
    hero_saw_flop = Column(Boolean, default=False)
    hero_c_bet_opp = Column(Boolean, default=False) # Opportunity to C-bet
    hero_c_bet = Column(Boolean, default=False)     # Did C-bet
    
    # Aggression & Showdown
    hero_af_bets = Column(Integer, default=0)       # Count of bets/raises
    hero_af_calls = Column(Integer, default=0)      # Count of calls
    hero_saw_showdown = Column(Boolean, default=False)
    hero_won_at_showdown = Column(Boolean, default=False)
    
    raw_text = Column(Text)
    processed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
