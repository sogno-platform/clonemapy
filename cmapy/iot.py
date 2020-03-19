"""
This module wraps around paho.mqtt.client
"""
import paho.mqtt.client as mqtt
import queue

def on_connect(client, userdata, flags, rc):
    pass

def on_message(client, userdata, msg):
    """
    add received mqtt message to message queue
    """
    client.msg_in_queue.put(msg)

def mqtt_connect():
    """
    connect to broker, start listening for messages and return client
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mqtt", 1883, 60)
    client.msg_in_queue = queue.Queue(1000)
    client.loop_start()
    return client

def mqtt_disconnect(client):
    """
    disconnect from broker
    """
    client.loop_stop()
    client.disconnect()