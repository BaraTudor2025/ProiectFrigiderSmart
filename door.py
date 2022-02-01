from flask import g
from flask_mqtt import Mqtt
from main import mqtt

"""
flow:
 - clientul(usa/frigiderul): daca usa e deschisa, o data pe secunda, 
    trimite unghiul la care usa este deschisa {intre 0 si 90, unde 0 este inchis}
 - server: (valori-default) daca trec 3 secunde AND unghiul ramane acelasi +- un epsilon(=1.0) AND < 15 grade
    atunci inchide usa
 - clientul poate modifica unghiul de inchidere cu o valoare intre 15, 45 si numarul de secunde de asteptat (intre 3 si 15)
    la topicul /door/set/angle si /door/set/seconds

 - clientul: publish la o secunda la /door/angle: <angle>
 - server: subscribe la /door/angle: <angle>

 - payloadul mesajului este irelevant, prin faptul ca am transmis la topicul /door/close usa se inchide
 - client: subscribe la /door/close, 
 - server: publish la /door/close
"""

angle_to_close = 15
seconds_to_wait = 3

# return true if the door needs to close
def door_needs_to_close(new_angle: float) -> bool:
    global angle_to_close, seconds_to_wait
    angles: list = g.get('angles')
    if angles == None:
        g['angles'] = [new_angle]
    else:
        angles.append(new_angle)
        # se presupuna ca distanta intre mesaje este de 1 secunda, deci len == time
        if len(angles) > seconds_to_wait:
            angles.pop(0)
        if len(angles) == seconds_to_wait:
            # sa fie toate sub <angle_to_close>
            for a in angles:
                if a > angle_to_close:
                    return False
            # eroarea de masurare pt float (daca exista) sa fie sub 1 grad
            dif = 0
            for i in range(0, len(angles) - 1):
                dif += (angles[i] - angles[i+1])
            return abs(dif) < 1
    return False

def mqtt_subscribe():
    def handle(client, userdata, msg):
        global angle_to_close, seconds_to_wait
        if msg.topic == '/door/angle':
            new_angle = float(msg.payload.decode())
            if door_needs_to_close(new_angle):
                mqtt.publish('/door/close', True, qos=2)
                g.pop('angles')

        elif msg.topic == '/door/set/angle':
            angle = int(msg.payload.decode())
            if angle >= 15 and angle <= 45:
                angle_to_close = angle
        elif msg.topic == '/door/set/seconds':
            sec = int(msg.payload.decode())
            if sec >= 3 and sec <= 15:
                seconds_to_wait = sec

    mqtt.on_message = handle
    mqtt.subscribe('/door/angle', qos=2)
    mqtt.subscribe('/door/set/angle', qos=2)
    mqtt.subscribe('/door/set/seconds', qos=2)

