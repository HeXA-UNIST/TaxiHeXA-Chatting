from flask import Flask, json, request, g, session, jsonify
import requests
from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, get_chat_all

from flask_socketio import SocketIO, join_room, leave_room, emit

def init_app():
    app = Flask(__name__)
    # socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*")
    socketio = SocketIO(cors_allowed_origins="*")
    socketio.init_app(app)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    cors.init_app(app)

    return app, socketio

app, socketio = init_app()
engine, get_db = init_db()

# 연결이 끊어질때 db close
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@socketio.on('join')
def handle_join(data):
    room_id = data["room_id"]

    is_authenticated = bool(session("is_authenticated", False))
    nickname = session.get("nickname", "")

    if is_authenticated:
        join_room(room_id)
        emit('receive_all_chatting', {"chat": get_chat_all(get_db(), room_id)}, to=room_id)
        emit('receive_new_participant', {"user": nickname}, to=room_id, broadcast=True)
    else:
        emit('warning')

@socketio.on('leave')
def handle_leave(data):
    room_id = data['room_id']
    nickname = session.get("nickname", "")

    leave_room(room_id)
    emit('receive_leave_participant', {"user": nickname}, to=room_id, broadcast=True)

@socketio.on('send_message')    # When got message from user
def handle_message(data):
    nickname = session.get("nickname", "")
    user_id = session.get("user_id", "")

    room_id = data['room_id']
    create_chat(get_db(), writer=nickname, room_id=room_id, content=data['content'], user_id=user_id)
    emit('receive_message', {'content': data["content"], 'user': nickname}, to=room_id, broadcast=True)

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", port=8081, debug=True)