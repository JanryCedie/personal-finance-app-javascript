from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import datetime
import models
from database import SessionLocal, engine
from sqlalchemy import func

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models
class TransactionCreate(BaseModel):
    type: str
    amount: float
    description: str

class TransactionResponse(TransactionCreate):
    id: int
    date: datetime.datetime

    class Config:
        orm_mode = True

@app.post("/transactions/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[TransactionResponse])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@app.get("/report/weekly")
def get_weekly_report(db: Session = Depends(get_db)):
    # Group by week. SQLite doesn't have easy date trunctation, so we might fetch all (fine for small app)
    # or use Python to aggregate. For a simple app, let's fetch all and aggregate in Python for simplicity and correctness with SQLite.
    
    transactions = db.query(models.Transaction).all()
    weekly_data = {}
    
    for t in transactions:
        # Get week start date (Monday)
        week_start = t.date - datetime.timedelta(days=t.date.weekday())
        week_key = week_start.strftime("%Y-%m-%d")
        
        if week_key not in weekly_data:
            weekly_data[week_key] = {"credit": 0, "debit": 0, "balance": 0}
            
        if t.type == "credit":
            weekly_data[week_key]["credit"] += t.amount
            weekly_data[week_key]["balance"] += t.amount
        elif t.type == "debit":
            weekly_data[week_key]["debit"] += t.amount
            weekly_data[week_key]["balance"] -= t.amount
            
    # Convert to list
    report = [{"week": k, **v} for k, v in weekly_data.items()]
    # Sort by week
    report.sort(key=lambda x: x["week"])
    return report

@app.get("/report/breakdown")
def get_breakdown(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    breakdown = {"credit": {}, "debit": {}}
    
    for t in transactions:
        category = t.description.strip().capitalize() if t.description else "Uncategorized"
        type_key = t.type # "credit" or "debit"
        
        if type_key in breakdown:
            if category not in breakdown[type_key]:
                breakdown[type_key][category] = 0
            breakdown[type_key][category] += t.amount
            
    # Format for chart friendliness if needed, or just return the dict
    # Let's return a list of objects for easier consumption
    # { "type": "credit", "category": "Salary", "amount": 5000 }
    
    result = []
    for t_type, categories in breakdown.items():
        for cat, amount in categories.items():
            result.append({"type": t_type, "category": cat, "amount": amount})
            
    return result

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
