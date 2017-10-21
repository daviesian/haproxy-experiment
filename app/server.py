from flask import Flask, make_response, request, abort
import os
import uuid
import signal
import time

app = Flask(__name__)

up = False
sessions = set()

@app.route("/")
def hello():
    requested_session = request.args.get('s', request.cookies.get('SESSIONID'))
    sid = requested_session if requested_session in sessions else str(uuid.uuid4())
    sessions.add(sid)

    server = request.headers["X-Backend-Server"]

    resp = make_response("Hello from %s, session %s.\n\n%s" % (server, sid, request.headers))
    resp.headers["Content-Type"] = "text/plain"
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
    signal.signal(signal.SIGUSR1, lambda *a: wake())
    signal.signal(signal.SIGUSR2, lambda *a: sleep())
    app.run(host="0.0.0.0")