from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import db, parser, models, analytics

# Initialize database tables
db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="Action Tracker API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; refine for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-log/")
async def upload_log(
    file: UploadFile = File(...),
    database: Session = Depends(db.get_db)
):
    """
    Accepts a text file of hand histories, parses them, and saves to the database.
    """
    content = await file.read()
    content_str = content.decode("utf-8")
    
    parsed_hands = parser.parse_hand_history(content_str)
    
    hand_ids = []
    for hand_data in parsed_hands:
        # Check if hand already exists
        existing_hand = database.query(db.Hand).filter(
            db.Hand.game_no == hand_data["game_no"]
        ).first()
        if existing_hand:
            continue
            
        db_hand = db.Hand(**hand_data)
        database.add(db_hand)
        database.commit()
        database.refresh(db_hand)
        hand_ids.append(db_hand.id)
        
    return {
        "count": len(hand_ids),
        "hand_ids": hand_ids
    }


@app.get("/hands/", response_model=List[models.Hand])
def read_hands(
    skip: int = 0,
    limit: int = 100,
    database: Session = Depends(db.get_db)
):
    hands = database.query(db.Hand).offset(skip).limit(limit).all()
    return hands


@app.get("/stats/hero")
def get_hero_stats(database: Session = Depends(db.get_db)):
    """
    Returns aggregated HUD stats for the Hero.
    """
    return analytics.get_hero_stats(database)


@app.get("/stats/position")
def get_position_stats(database: Session = Depends(db.get_db)):
    """
    Returns HUD stats broken down by Hero's position.
    """
    return analytics.get_positional_stats(database)
