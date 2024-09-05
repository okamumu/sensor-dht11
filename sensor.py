import time
import RPi.GPIO as GPIO
import dht11
import datetime
import paho.mqtt.client as mqtt
import json

# configuration
json_file = 'config.json'
with open(json_file) as f:
    config = json.load(f)
    host = config['host']
    port = config['port']
    topic = config['topic']
    pin = config['pin']
    wait = config['wait']
    location = config['location']

# initialize GPIO
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin = pin)

# mqtt initialize
client = mqtt.Client()
client.connect(host, port=port)

# loop
try:
  client.loop_start()
  while True:
    result = instance.read()
    if result.is_valid():
      d = str(datetime.datetime.now())
      print("Last valid input: " + d)
      data = {
        'timestamp': d,
        'location': location,
        'temperature': result.temperature,
        'humidity': result.humidity
      }
      msg = json.dumps(data)
      print(msg)
      client.publish(topic, msg)
    time.sleep(wait)
except KeyboardInterrupt:
  GPIO.cleanup()
  client.disconnect()
