from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base

from src.database.database import engine

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, index=True)
    user_id = Column(String)
    nickname = Column(String, unique=True)
    content = Column(String)
    created_at = Column(DateTime, server_default=current_timestamp())

# 데이터베이스 생성
Base.metadata.create_all(bind=engine)