import functools, threading, flask

app = flask.Flask(__name__)

@app.route("/")
def index():
    return "."

def keep_alive():
    partial_run = functools.partial(app.run, host="0.0.0.0", port=8080)
    threading.Thread(target=partial_run).start()