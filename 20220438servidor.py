import json
import time
import threading

import paho.mqtt.client as mqtt

id = '21d3ce0e-04d7-4d16-9871-32e70fb7c5ab'

client_telemetry_topic = id + '20220438/telemetriaexame'
client_name = id + '20220438servidor'
server_command_topic = id + '20220438/comandosexame'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")


wait_time = 20

def send_relay_command(client, state):
    command = { 'estado_led_on' : state }
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

def control_relay(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)

    send_relay_command(client, True)
    time.sleep(wait_time)
    send_relay_command(client, False)

    time.sleep(wait_time)

    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['temp'] < 80:
        threading.Thread(target=control_relay, args=(client,)).start()
        
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)