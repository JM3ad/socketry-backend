from flask import Flask
from flask_socketio import SocketIO, emit

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

    return socketio

app = create_app()
socketio = create_socketio(app)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")