"""

"""
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import esp
esp.osdebug(None)
import gc
gc.collect()
from machine import Pin #  biblioteca machine
import json

class Assinar:
  def __init__(self, topico):

    self.led = Pin(27, Pin.OUT)
    self.mqtt_server = 'test.mosquitto.org'
    self.client_id = ubinascii.hexlify(machine.unique_id())
    self.topic_sub = topico.encode() #b'hello'


  def sub_cb(self,topic, msg):
    print((topic, msg))
    # aqui verifica a mensaem enviada
    try:
        dados = json.loads(msg.decode())
        print(dados)

        if topic == b'hello' and dados['cmd'] == 'on':
          self.led.value(1)
        if topic == b'hello' and dados['cmd'] == 'off':  
          self.led.value(0)
    except:
        print('Mensagem não valida')
  
  
  def connect_and_subscribe(self):
    #global client_id, mqtt_server, topic_sub
    client = MQTTClient(self.client_id, self.mqtt_server)
    client.set_callback(self.sub_cb)
    client.connect()
    client.subscribe(self.topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (self.mqtt_server, self.topic_sub))
    return client

  def restart_and_reconnect(self):
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

  def start(self):  
    try:
      client = self.connect_and_subscribe()
    except OSError as e:
      self.restart_and_reconnect()

    while True:
      try:
        client.check_msg()        
      except OSError as e:
        self.restart_and_reconnect()