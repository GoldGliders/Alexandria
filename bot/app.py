from flask import Flask
import logging
import logging.handlers

LOGFILE = "/var/log/flask/access.log"

app = Flask(__name__)

handler = logging.handlers.RotatingFileHandler(LOGFILE)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler)

@app.route("/", methods=["GET"])
def index():
    return "This is flask app"

if __name__ == "__main__":
    app.run(debug=True)
