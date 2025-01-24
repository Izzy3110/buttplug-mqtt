from flask_socketio import emit

from app.app import create_app
from app.blueprints.general import bp_general
from app.extensions.bootstrap import bootstrap
from app.extensions.socketio import socketio

app = create_app()
app.register_blueprint(bp_general)
socketio.init_app(app)
bootstrap.init_app(app)


@socketio.on('connect')
def test_connect(auth):
    print(auth)
    emit('all_broadcast', {'data': 'Connected'})
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect(reason):
    emit('all_broadcast', {'data': 'Client disconnected'})
    print('Client disconnected, reason:', reason)


@socketio.on('mouse_create_point')
def handle_mouse_create_point(data):
    print(f"mouse_create_point: Mouse clicked at: {data}")
    # Emit the coordinates back to all connected clients
    emit('mouse_coordinates', data, broadcast=True)


@socketio.on('mouse_move_point')
def handle_mouse_move_point(data):
    print(f"mouse_move_point: Mouse clicked at: {data}")
    # Emit the coordinates back to all connected clients
    emit('mouse_coordinates', data, broadcast=True)


@socketio.on('mouse_move')
def handle_mouse_move(data):
    print(f"Mouse clicked at: {data}")
    # Emit the coordinates back to all connected clients
    emit('mouse_coordinates', data, broadcast=True)


@socketio.on('mouse_click')
def handle_mouse_click(data):
    print(f"Mouse clicked at: {data}")
    # Emit the coordinates back to all connected clients
    emit('mouse_coordinates', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, port=5005, debug=True, allow_unsafe_werkzeug=True)
