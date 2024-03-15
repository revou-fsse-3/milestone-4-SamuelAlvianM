from models.base import Base
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func

from flask_login import UserMixin
import bcrypt


class User(Base, UserMixin):
    __tablename__ = 'users'

    user_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = mapped_column(String(200), nullable=False, unique=True)
    email = mapped_column(String(200), nullable=False, unique=True)
    password = mapped_column(String(200), nullable=False)
    created_at = mapped_column(DateTime(timezone=True))
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())


    accounts = relationship("Account", backref="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = bcrypt.hashpw( password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def get_id(self):
        return str(self.user_id)
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }