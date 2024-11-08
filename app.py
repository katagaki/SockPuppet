from datetime import datetime
from uuid import uuid4

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__, static_url_path="", static_folder="web/build", template_folder="web/build")
app.config["SECRET_KEY"] = str(uuid4())

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, path="sync", cors_allowed_origins="*")


@app.route("/")
def serve_react_app():
    return render_template("index.html")


@app.route("/ping", methods=["POST"])
def http_call():
    return jsonify({}, 200)


@socketio.on("connect")
def connected():
    join_room("Room 1", request.sid)


@socketio.on("data")
def handle_message(data):
    if str(data) == "immediate":
        socketio.send("This response was generated immediately.", to="Room 1")

    elif str(data) == "delayed":
        def send_time_at_regular_intervals():
            socketio.sleep(3)
            date_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            socketio.send(f"This response was generated at {date_now}.", to="Room 1")

        socketio.start_background_task(send_time_at_regular_intervals)


@socketio.on("heartbeat")
def heartbeat():
    socketio.send(f"Heartbeat response to keep connection alive.", to="Room 1")


@socketio.on("disconnect")
def disconnected():
    leave_room("Room 1", request.sid)
