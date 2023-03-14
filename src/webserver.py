from flask import Flask
from threading import Thread

app = Flask(__app__)

@app.route("/")
def index():
  return 200

def start_webserver():
  Thread(target=app.run, args=("0.0.0.0",), kwargs={"port": 8080}).start()
