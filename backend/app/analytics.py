from sqlalchemy.orm import Session
from .db import Hand
from sqlalchemy import func
from typing import Dict, Any

def get_hero_stats(db: Session, filters: Dict[str, Any] = None):
    """
    Calculates detailed HUD statistics for the Hero.
    Optional filters (like hero_position) can be applied.
    """
    query = db.query(Hand)
    if filters:
        for key, value in filters.items():
            query = query.filter(getattr(Hand, key) == value)
            
    total_hands = query.count()
    if total_hands == 0:
        return {}

    # 1. Pre-Flop Stats
    vpip_count = query.filter(Hand.hero_vpip == True).count()
    pfr_count = query.filter(Hand.hero_pfr == True).count()
    three_bet_count = query.filter(Hand.hero_three_bet == True).count()
    
    # 2. Post-Flop Stats
    saw_flop_count = query.filter(Hand.hero_saw_flop == True).count()
    cbet_opp_count = query.filter(Hand.hero_c_bet_opp == True).count()
    cbet_count = query.filter(Hand.hero_c_bet == True).count()
    
    # 3. Aggression
    total_bets = query.with_entities(func.sum(Hand.hero_af_bets)).scalar() or 0
    total_calls = query.with_entities(func.sum(Hand.hero_af_calls)).scalar() or 0
    af = round(total_bets / total_calls, 2) if total_calls > 0 else total_bets

    # 4. Showdown Stats
    wtsd_count = query.filter(Hand.hero_saw_showdown == True).count()
    wsd_count = query.filter(Hand.hero_won_at_showdown == True).count()

    return {
        "summary": {
            "total_hands": total_hands,
            "win_rate": round((query.filter(Hand.hero_result > 0).count() / total_hands) * 100, 2),
            "net_result": query.with_entities(func.sum(Hand.hero_result)).scalar() or 0
        },
        "preflop": {
            "vpip": round((vpip_count / total_hands) * 100, 2),
            "pfr": round((pfr_count / total_hands) * 100, 2),
            "three_bet": round((three_bet_count / total_hands) * 100, 2),
        },
        "postflop": {
            "cbet": round((cbet_count / cbet_opp_count) * 100, 2) if cbet_opp_count > 0 else 0,
            "af": af,
        },
        "showdown": {
            "wtsd": round((wtsd_count / saw_flop_count) * 100, 2) if saw_flop_count > 0 else 0,
            "wsd": round((wsd_count / wtsd_count) * 100, 2) if wtsd_count > 0 else 0,
        }
    }

def get_positional_stats(db: Session):
    """
    Returns a dictionary of stats broken down by Hero's position.
    """
    positions = db.query(Hand.hero_position).distinct().all()
    breakdown = {}
    
    for pos_tuple in positions:
        pos_name = pos_tuple[0]
        if not pos_name:
            continue
        breakdown[pos_name] = get_hero_stats(db, filters={"hero_position": pos_name})
        
    return breakdown
