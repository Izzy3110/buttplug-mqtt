from control_panel.app.app import create_app
from control_panel.app.blueprints.general import bp_general
from control_panel.app.extensions.bootstrap import bootstrap
from control_panel.app.extensions.socketio import socketio

app = create_app()
app.register_blueprint(bp_general)
socketio.init_app(app)
bootstrap.init_app(app)


if __name__ == '__main__':
    socketio.run(app, port=5005, debug=True, allow_unsafe_werkzeug=True)
