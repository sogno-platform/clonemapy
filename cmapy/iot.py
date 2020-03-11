import paho.mqtt.client as mqtt
import queue

def on_connect(client, userdata, flags, rc):
    pass

def on_message(client, userdata, msg):
    pass

def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mqtt", 1883, 60)
    msg_in = queue.Queue(1000)
    return client, msg_in