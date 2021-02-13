from pytest import fixture
from app.app import app, socketio
from dotenv import load_dotenv, find_dotenv

@fixture
def socket_client():
    env_file = find_dotenv('.env.test')
    load_dotenv(env_file, override=True)
    return socketio.test_client(app)

@fixture
def connected_socket_client(socket_client):
    socket_client.get_received()
    return socket_client

def test_socket_connects(socket_client):
    initial_response = socket_client.get_received()
    assert len(initial_response) == 1
    assert initial_response[0]['name'] == 'seen'

def test_join_room_responds(connected_socket_client):
    connected_socket_client.emit('join_room', {'name': 'test-name', 'room': 'a-room-id'})
    response = connected_socket_client.get_received()
    assert len(response) == 1
    assert response[0]['name'] == 'message'
    assert 'test-name' in response[0]['args']