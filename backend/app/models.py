from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class HandBase(BaseModel):
    game_no: str
    table_name: Optional[str] = None
    game_type: Optional[str] = None
    stakes: Optional[str] = None
    hero_cards: Optional[str] = None
    hero_position: Optional[str] = None
    hero_result: Optional[int] = 0
    
    # Pre-Flop
    hero_vpip: Optional[bool] = False
    hero_pfr: Optional[bool] = False
    hero_three_bet: Optional[bool] = False
    hero_fold_to_three_bet: Optional[bool] = False
    
    # Post-Flop
    hero_saw_flop: Optional[bool] = False
    hero_c_bet_opp: Optional[bool] = False
    hero_c_bet: Optional[bool] = False
    
    # Stats
    hero_af_bets: Optional[int] = 0
    hero_af_calls: Optional[int] = 0
    hero_saw_showdown: Optional[bool] = False
    hero_won_at_showdown: Optional[bool] = False
    
    raw_text: Optional[str] = None


class HandCreate(HandBase):
    pass


class Hand(HandBase):
    id: int
    processed_at: datetime

    model_config = ConfigDict(from_attributes=True)
