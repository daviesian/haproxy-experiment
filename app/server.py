from flask import Flask, make_response, request, abort
import os
import uuid

app = Flask(__name__)

up = True
sessions = set()

@app.route("/")
def hello():
    requested_session = request.args.get('s', request.cookies.get('SESSIONID'))
    sid = requested_session if requested_session in sessions else str(uuid.uuid4())
    sessions.add(sid)
    resp = make_response("Hello from %s, session %s" % (os.environ.get("SERVER_ID"), sid))
    resp.set_cookie('SESSIONID', sid)
    return resp

@app.route("/_status")
def status():
    if up:
        return "OK"
    else:
        return "Nope", 404 #abort(404)

@app.route("/sleep")
def sleep():
    global up
    up = False
    return ""

@app.route("/wake")
def wake():
    global up
    up = True
    return ""

@app.route("/die")
def die():
    request.environ.get('werkzeug.server.shutdown')()
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0")