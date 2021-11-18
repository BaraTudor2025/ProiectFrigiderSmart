from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import eventlet
import json
import time

def mqtt_thread(mqtt, app):
    count = 0
    while True:
        time.sleep(1)


def main():
    eventlet.monkey_patch()
    app = Flask("frigider-smart", instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    # register HTTP API paths
    # db.init_app(app)
    # app.register_blueprint(auth.bp)

    # start MQTT service
    mqtt = Mqtt(app)
    thread = Thread(target=mqtt_thread, args=(mqtt, app))
    thread.daemon = True
    #thread.start()

    # start HTTP service
    socketio = SocketIO(app, async_mode="eventlet")
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)



if __name__ == "__main__":
    main()