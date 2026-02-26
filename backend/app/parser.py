import re
from typing import List, Dict, Any

def parse_hand_history(content: str) -> List[Dict[str, Any]]:
    """
    Parses a raw GGPoker hand history file into a list of structured hands.
    Extracts high-fidelity HUD stats for analytical depth.
    """
    hands_raw = re.split(r'(?=#Game No : |Poker Hand #)', content)
    
    parsed_hands = []
    for raw_hand in hands_raw:
        if not raw_hand.strip():
            continue
            
        hand_data = {
            "raw_text": raw_hand.strip(),
            "game_no": None,
            "table_name": None,
            "game_type": None,
            "stakes": None,
            "hero_cards": None,
            "hero_position": None,
            "hero_result": 0,
            "hero_vpip": False,
            "hero_pfr": False,
            "hero_three_bet": False,
            "hero_fold_to_three_bet": False,
            "hero_saw_flop": False,
            "hero_c_bet_opp": False,
            "hero_c_bet": False,
            "hero_af_bets": 0,
            "hero_af_calls": 0,
            "hero_saw_showdown": False,
            "hero_won_at_showdown": False
        }
        
        # Metadata parsing
        header_match = re.search(r'Poker Hand #(\w+): (.*?) - (.*?) - (.*)', raw_hand)
        if header_match:
            hand_data["game_no"] = header_match.group(1)
            hand_data["game_type"] = header_match.group(2).strip()
            hand_data["stakes"] = header_match.group(3).strip()
        table_match = re.search(r"Table '(.*?)'", raw_hand)
        if table_match:
            hand_data["table_name"] = table_match.group(1)

        # Hero Cards
        cards_match = re.search(r'Dealt to Hero \[(.*?)\]', raw_hand)
        if cards_match:
            hand_data["hero_cards"] = cards_match.group(1)

        # Street-by-street Analysis
        sections = re.split(r'\*\*\* (HOLE CARDS|FLOP|TURN|RIVER|SHOWDOWN|SUMMARY) \*\*\*', raw_hand)
        
        # Helper to get section content
        def get_section(name):
            for i in range(len(sections)):
                if sections[i] == name and i + 1 < len(sections):
                    return sections[i+1]
            return ""

        preflop = get_section("HOLE CARDS")
        flop = get_section("FLOP")
        turn = get_section("TURN")
        river = get_section("RIVER")
        showdown = get_section("SHOWDOWN")
        summary = get_section("SUMMARY")

        # 1. Pre-Flop Analysis (VPIP, PFR, 3B)
        if preflop:
            # Count actions to detect 3-bet
            # Simplification: A 3-bet is the 3rd bet (1=blind, 2=raise, 3=re-raise)
            raises = re.findall(r': raises', preflop)
            hero_actions = re.findall(r'Hero: (calls|raises)', preflop)
            
            if "raises" in [a for a in hero_actions]:
                hand_data["hero_vpip"] = True
                hand_data["hero_pfr"] = True
                
                # Check if Hero's raise was a 3-bet (meaning someone else raised before)
                first_raise_match = re.search(r'(\w+): raises', preflop)
                if first_raise_match and first_raise_match.group(1) != "Hero":
                    # Someone else raised first, if Hero raised after, it's a 3-bet
                    hero_raise_match = re.search(r'Hero: raises', preflop)
                    if hero_raise_match and preflop.find("Hero: raises") > preflop.find(first_raise_match.group(0)):
                        hand_data["hero_three_bet"] = True
            elif "calls" in [a for a in hero_actions]:
                hand_data["hero_vpip"] = True

            # Fold to 3-bet: Hero raises, then someone else re-raises, then Hero folds
            if hand_data["hero_pfr"]:
                opp_3bet_match = re.search(r'Hero: raises.*?(\w+): raises.*?Hero: folds', preflop, re.DOTALL)
                if opp_3bet_match:
                    hand_data["hero_fold_to_three_bet"] = True

        # 2. Post-Flop Analysis (C-Bet, Saw Flop)
        if flop:
            hand_data["hero_saw_flop"] = True
            
            # C-Bet: PFR aggressor bets on the flop
            if hand_data["hero_pfr"]:
                hand_data["hero_c_bet_opp"] = True
                # Check if Hero bets on the flop (simplified: Hero's first action is a bet)
                if re.search(r'Hero: bets', flop):
                    hand_data["hero_c_bet"] = True

        # 3. Aggression Factor (AF) - Collect across all streets
        for street in [preflop, flop, turn, river]:
            if street:
                hand_data["hero_af_bets"] += len(re.findall(r'Hero: raises', street))
                hand_data["hero_af_bets"] += len(re.findall(r'Hero: bets', street))
                hand_data["hero_af_calls"] += len(re.findall(r'Hero: calls', street))

        # 4. Showdown Performance
        if showdown:
            hand_data["hero_saw_showdown"] = True
        
        # 5. Summary Results and Position Refinement
        if summary:
            # Match Hero's line in summary to get position and outcome
            # Possible: Hero (button), Hero (small blind), Hero (big blind), or just Hero
            hero_sum_match = re.search(r'Seat \d+: Hero (.*?)(folded|showed|won|lost)(.*)', summary)
            if hero_sum_match:
                raw_pos = hero_sum_match.group(1).strip()
                if not raw_pos:
                    # If no explicit label like (button), it's a non-blind/button position
                    # We can label these as 'Other' or try to infer from seat count
                    hand_data["hero_position"] = "UTG/MP/CO"
                else:
                    hand_data["hero_position"] = raw_pos.strip("()")
                
                outcome = hero_sum_match.group(2)
                details = hero_sum_match.group(3)
                
                if outcome == "won" or "won (" in details:
                    hand_data["hero_won_at_showdown"] = True if hand_data["hero_saw_showdown"] else False
                    win_match = re.search(r'won \(?([\d,]+)\)?', details)
                    if win_match:
                        hand_data["hero_result"] = int(win_match.group(1).replace(",", ""))

        if hand_data["game_no"]:
            parsed_hands.append(hand_data)
            
    return parsed_hands

