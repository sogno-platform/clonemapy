import paho.mqtt.client as mqtt
import queue

def on_connect(client, userdata, flags, rc):
    pass

def on_message(client, userdata, msg):
    client.msg_in_queue.put(msg)

def mqtt_connect():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mqtt", 1883, 60)
    client.msg_in_queue = queue.Queue(1000)
    client.loop_start()
    return client

def mqtt_disconnect(client):
    client.loop_stop()
    client.disconnect()