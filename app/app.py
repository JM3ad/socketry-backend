from flask import Flask
from flask_socketio import SocketIO, emit, send, join_room, leave_room

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/healthcheck')
    def healthcheck():
        return 'Healthy'

    return app

def create_socketio(app):
    socketio = SocketIO(app, cors_allowed_origins="*")

    @socketio.on('message')
    def handle_message(data):
        print('received message: ' + data)
        emit('response', data)
    
    @socketio.on('connect')
    def test_connect():
        emit('seen', {'message': 'connected'})

    @socketio.on('join_room')
    def on_join(data):
        name = data['name']
        room = data['room']
        join_room(room)
        send(name + ' has entered ' + room, room=room)

    @socketio.on('leave_room')
    def on_leave(data):
        name = data['name']
        room = data['room']
        leave_room(room)
        send(name + ' has left ' + room, room=room)

    return socketio

app = create_app()
socketio = create_socketio(app)