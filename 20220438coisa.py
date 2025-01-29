from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)
import time
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt
import json
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed


id = '21d3ce0e-04d7-4d16-9871-32e70fb7c5ab'

client_name = id + '20220438coisa'
client_telemetry_topic = id + '20220438/telemetriaexame'
server_command_topic = id + '20220438/comandosexame'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

led = GroveLed(4)
sensor = DHT("11", 1)

mqtt_client.loop_start()

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['estado_led_on']:
        led.on()
    else:
        led.off()
        
mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command 

print("MQTT connected!")



while True:
    _, valortemperatura = sensor.read()
    telemetry = json.dumps({'temp' : valortemperatura})

    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5);