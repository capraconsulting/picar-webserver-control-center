#!/usr/bin/env python

from __future__ import print_function

import logging

from flask import Flask, request, json, abort
from flask_sockets import Sockets

from controls import PicarControl
from controls import ActionParseFailedException, PicarModulesUnavailableException
from controls import get_control_action

app = Flask(__name__)
sockets = Sockets(app)

logger = logging.getLogger(__name__)

# TODO: Replace this with a hash string or something
WEBSOCKET_SECURITY_TOKEN = "secret"


@sockets.route("/picar_action")
def ping(ws):
    token = request.args.get('token')
    if token != WEBSOCKET_SECURITY_TOKEN:
        abort(401)
    try:
        picar_instance = PicarControl()
    except PicarModulesUnavailableException:
        logging.error("Picar modules unavailable. Assuming running locally")

    while not ws.closed:
        # Block body executed per received message from the connected client
        message = ws.receive()
        print(request.headers)
        data = json.loads(message)
        try:
            action = get_control_action(data)
        except ActionParseFailedException:
            message = json.dumps({"error": "No action could be parsed from the input"})
        ws.send(message)



@app.route("/")
def index():
    return "Here be the root of all"


@app.route("/start_engine", methods=["POST"])
def start_engine():
    data = {
        "success": True
    }
    return json.jsonify(data)


@app.route("/directions", methods=["POST"])
def drive_car():
    incoming_data = request.get_json()
    print(incoming_data)
    data = {
        "success": True
    }
    return json.jsonify(data)


if __name__ == "__main__":
    try:
        import netifaces
        host_address = netifaces.ifaddresses(
            "wlan0")[netifaces.AF_INET][0]["addr"]
        logging.info("Running server on address {}".format(host_address))
    except:
        logging.warning("Could not get address of the INET0 interface." +
              "Fallingback to running on loopback interface (127.0.0.1)")
        host_address = "127.0.0.1"

    # app.run(host=host_address)

    # Run with WebsocketHandler
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer((host_address, 5000), app,
                               handler_class=WebSocketHandler)
    server.serve_forever()
