import os
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine, Hand
from app.parser import parse_hand_history

# Initialize database
Base.metadata.create_all(bind=engine)

def repopulate():
    file_path = "testdata/GG20260102-0122 - #19 26 The Year Begins.txt"
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, "r") as f:
        content = f.read()

    parsed_hands = parse_hand_history(content)
    print(f"Total hands parsed: {len(parsed_hands)}")

    db = SessionLocal()
    try:
        for hand_data in parsed_hands:
            db_hand = Hand(**hand_data)
            db.add(db_hand)
        
        db.commit()
        print(f"Stored {len(parsed_hands)} hands with Hero POV data.")

        # Query and display samples
        stored_hands = db.query(Hand).filter(Hand.hero_cards != None).limit(5).all()
        print("\n--- Hero POV Samples from Database ---")
        for h in stored_hands:
            print(f"ID: {h.id} | Game: {h.game_no} | Cards: {h.hero_cards}")
            print(f"Pos: {h.hero_position} | Result: {h.hero_result}")
            print("-" * 40)

    finally:
        db.close()

if __name__ == "__main__":
    repopulate()
