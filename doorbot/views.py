from doorbot import app, auth
from jsonify import jsonify as jsondecorate
from flask import jsonify, Response

@app.route('/')
def base():
    return Response("Hello World")

@app.route('/open')
@auth.login_required
def bad_open():
    app.log.warn("Invalid Door Open Action by {user}".format(
        user=auth.username()
    ))
    return Response("Please use a valid doorid ({})".format(app.doors.keys()))

@app.route('/open/<doorid>')
@auth.login_required
def open(doorid):
    if doorid not in app.doors.keys():
        return bad_open()

    status, msg = app.doors[doorid].open()
    if status is None:
        response = "Door already open: {}".format(msg)
    elif status is True:
        response = "OK: {}".format(msg)
    else:
        response = msg

    app.log.info("Door Open Action by {user}:{response}".format(
        user=auth.username(),
        response=response
    ))
    return Response(response)

@app.route('/status')
@auth.login_required
def status():
    return Response("Hello {}: The door config is {}".format(auth.username(),app.doors))
