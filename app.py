from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys
import io

app = Flask(__name__)
socketio = SocketIO(app)


# A function to execute Python code and capture the output
def execute_code(code):
    try:
        # Redirect stdout to capture print statements
        captured_output = io.StringIO()
        sys.stdout = captured_output
        # Execute the provided code
        exec(code)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()
    except Exception as e:
        return str(e)


# Serve the index.html page
@app.route("/")
def index():
    return render_template("index.html")


# Handle the incoming code from the client and send back the output
@socketio.on("code_change")
def handle_code_change(code):
    output = execute_code(code)
    emit("output", {"output": output})


if __name__ == "__main__":
    socketio.run(app, debug=True)
