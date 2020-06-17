import logging

from flask import jsonify, Response

from doorbot.app import app, auth


@app.route('/')
def base():
    return Response("Hello World")


@app.route('/open')
@auth.login_required
def open_base():
    app.log.warn("Invalid Door Open Action by {user}".format(
        user=auth.username()
    ))
    return jsonify(action='open', option='', status=False, msg="Invalid Door or User", user=auth.username())


@app.route('/open/<doorid>')
@auth.login_required
def open_door(doorid):
    if doorid not in app.doors.keys():
        return jsonify(action='open', option=doorid, status=False, msg="Invalid Door", user=auth.username())

    status, msg = app.doors[doorid].open()
    if status is None:
        response = "Door already open: {}".format(msg)
    elif status is True:
        response = "OK: {}".format(msg)
    else:
        response = msg

    logging.info("Door Open Action by {user}:{response}".format(
        user=auth.username(),
        response=response
    ))
    return jsonify(action='open', option=doorid, status=bool(status), msg=response, user=auth.username())


@app.route('/status')
@auth.login_required
def status():
    return jsonify(action='status', option=None, status=None, msg=repr(app.doors), user=auth.username())
