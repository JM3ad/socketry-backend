from pytest import fixture
from app.app import app, socketio
from dotenv import load_dotenv, find_dotenv

@fixture
def socket_client():
    env_file = find_dotenv('.env.test')
    load_dotenv(env_file, override=True)
    return socketio.test_client(app)

socket_client_2 = socket_client

def test_socket_connects(socket_client):
    # When
    initial_response = socket_client.get_received()

    # Then
    assert len(initial_response) == 1
    assert initial_response[0]['name'] == 'seen'

def test_join_room_responds(socket_client):
    # Given
    clear_responses(socket_client)

    # When
    join_room(socket_client)

    # Then
    response = socket_client.get_received()
    assert len(response) == 1
    assert response[0]['name'] == 'message'
    assert 'test-name' in response[0]['args']

def test_leave_room_responds_to_other_room_members(socket_client, socket_client_2):
    # Given
    join_room(socket_client)
    join_room(socket_client_2)
    clear_responses(socket_client)
    clear_responses(socket_client_2)

    # When
    leave_room(socket_client)

    # Then
    client_1_response = socket_client.get_received()
    assert len(client_1_response) == 0

    client_2_response = socket_client_2.get_received()
    assert client_2_response[0]['name'] == 'message'
    assert 'test-name' + ' has left ' in client_2_response[0]['args']

def join_room(client):
    client.emit('join_room', {'name': 'test-name', 'room': 'a-room-id'})

def leave_room(client):
    client.emit('leave_room', {'name': 'test-name', 'room': 'a-room-id'})

def clear_responses(client):
    client.get_received()