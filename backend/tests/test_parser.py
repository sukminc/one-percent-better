from app.parser import parse_hand_history

def test_parse_hand_history():
    raw_content = """#Game No : G123456789
#Table Name : Table Blue
#Game Type : No Limit Hold'em
#Stakes : $0.05/$0.10
Player 1 posts small blind $0.05
Player 2 posts big blind $0.10
...

#Game No : G987654321
#Table Name : Table Red
#Game Type : No Limit Hold'em
#Stakes : $0.10/$0.20
Player 3 posts small blind $0.10
Player 4 posts big blind $0.20
...
"""
    hands = parse_hand_history(raw_content)
    
    assert len(hands) == 2
    assert hands[0]["game_no"] == "G123456789"
    assert hands[0]["table_name"] == "Table Blue"
    assert hands[0]["game_type"] == "No Limit Hold'em"
    assert hands[0]["stakes"] == "$0.05/$0.10"
    
    assert hands[1]["game_no"] == "G987654321"
    assert hands[1]["table_name"] == "Table Red"
    assert hands[1]["game_type"] == "No Limit Hold'em"
    assert hands[1]["stakes"] == "$0.10/$0.20"
