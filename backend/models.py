from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True) # "credit" or "debit"
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
