#!/usr/bin/env python

from __future__ import print_function

import logging

from flask import Flask, request, json, abort
from flask_sockets import Sockets

from controls import PicarControl
from controls.controls_mock import PicarControlMock
from controls import ActionParseFailedException
from controls import PicarModulesUnavailableException
from controls import get_control_action

app = Flask(__name__)
sockets = Sockets(app)

logger = logging.getLogger(__name__)

# TODO: Replace this with a hash string or something
WEBSOCKET_SECURITY_TOKEN = "verysecrettoken"

DEBUG = True


@app.route("/")
def index():
    return "Here be the root of all"


@app.route("/blue")
def another():
    return "Here be the BLUE root of all"


@sockets.route("/picar_action")
def action(ws):
    token = request.args.get('token')
    if token != WEBSOCKET_SECURITY_TOKEN:
        abort(401)
    try:
        picar_instance = PicarControl(debug=DEBUG)
    except PicarModulesUnavailableException:
        logging.error(
            "Picar modules unavailable. Using the mock module instead")
        picar_instance = PicarControlMock()

    while not ws.closed:
        # Block body executed per received message from the connected client
        message = ws.receive()
        data = json.loads(message)
        try:
            action = get_control_action(data)
            picar_instance.drive_from_action(action)
        except ActionParseFailedException:
            message = json.dumps({
                "error":
                "No action could be parsed from the input"
            })
        ws.send(message)

    picar_instance.shut_down()


if __name__ == "__main__":
    try:
        import netifaces
        host_address = netifaces.ifaddresses("wlan0")[netifaces.AF_INET][0][
            "addr"]
        print("Running server on address {}".format(host_address))
    except:
        logging.warning(
            "Could not get address of the INET0 interface." +
            "Fallingback to running on loopback interface (127.0.0.1)")
        # host_address = "127.0.0.1"
        host_address = "0.0.0.0"

    # Run with WebsocketHandler
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(
        (host_address, 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
