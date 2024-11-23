from sqlalchemy.orm import Session
from src.database.models import *

def create_chat(db: Session, nickname: str, room_id: str, content: str, user_id: str):
    content = Chat(nickname=nickname, content=content, room_id=room_id, user_id=user_id)
    db.add(content)
    db.commit()
    return content

def get_chat_all(db: Session, room_id: str):
    chats = db.query(Chat).filter(Chat.room_id == room_id).all()
    if chats == None:
        return []
    else:
        chat_data = []
        for i in chats:
            res = {}
            res["nickname"] = i.nickname
            res["content"] = i.content
            chat_data.append(res)   # chat_data: [{"nickname":"who", "chat":"chat content", "time", "chatting 시각"}, {...}, ...]
        return chat_data

