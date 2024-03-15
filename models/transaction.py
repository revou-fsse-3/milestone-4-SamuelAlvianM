from models.base import Base
from sqlalchemy import Enum, Integer, String, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.account_id", ondelete="CASCADE"))
    to_account_id = mapped_column(Integer, ForeignKey("accounts.account_id", ondelete="CASCADE"))
    type_transaction = mapped_column(Enum('deposit', 'withdrawal', 'transfer'), nullable= False)
    amount = mapped_column(DECIMAL(10, 2), nullable=False)
    description = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    sender = relationship("Account", foreign_keys=[from_account_id], back_populates="transactions_as_sender")
    receiver = relationship("Account", foreign_keys=[to_account_id], back_populates="transactions_as_receiver")

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'
    
    def serialize(self):
        return {
            "transaction_id": self.transaction_id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "type_transaction": self.type_transaction,
            "amount": str(self.amount),
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }