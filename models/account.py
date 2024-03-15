from datetime import datetime
from models.base import Base
from sqlalchemy import  Enum, Float, ForeignKey, Integer, String, Text, DateTime, func
from models.user import User
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.sql import func


class Account(Base):
    __tablename__ = 'accounts'

    account_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    account_type = mapped_column(Enum('savings', 'trading', 'platinum'), nullable=False)
    account_number = mapped_column(String(100), nullable=False, unique=True)
    balance = mapped_column(Float(10, 2), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # user = relationship("User", back_populates="accounts")

    transactions_as_sender = relationship("Transaction", foreign_keys="[Transaction.from_account_id]", back_populates="sender")
    transactions_as_receiver = relationship("Transaction", foreign_keys="[Transaction.to_account_id]", back_populates="receiver")


    def serialize(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "account_type": self.account_type,
            "account_number": self.account_number,
            "balance": float(self.balance), 
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<Account {self.account_id}, user_id={self.user_id}, account_type={self.account_type}, account_number={self.account_number}, balance={self.balance}>'