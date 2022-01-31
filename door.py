import db
from flask_mqtt import Mqtt
from main import mqtt

"""
flow:
 - clientul(usa/frigiderul): daca usa e deschisa, o data pe secunda, 
    trimite unghiul la care usa este deschisa {angle:<nr-in-grade(0,90)>}
 - server: daca trec 5 secunde AND unghiul ramane acelasi +- un epsilon AND < 15 grade
    atunci inchide usa
    SAU daca > 15 si trec 5 minute inchide usa

 - clientul: publish la o secunda /python/mqtt/opendoor - 'angle:<nr>'
 - server: subscribe la /python/mqtt/opendoor - 'angle:<nr>'

 - client: subscribe la /opendoor - 'close'
 - server: publish la /opendoor - 'close'
"""

def start_timer():
    def handle(client, userdata, msg):
        if msg.topic == 'python/mqtt/opendoor':
            str = msg.payload.decode()
        pass
    mqtt.on_message(handle)
    mqtt.subscribe('python/mqtt/opendoor')
