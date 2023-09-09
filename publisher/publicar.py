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
import onewire, ds18x20
from machine import Pin #  biblioteca machine


class Publicar:
  def __init__(self):
    self.ds_pin = machine.Pin(22)
    self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds_pin))
    self.roms = self.ds_sensor.scan()
    print('Found DS devices: ', self.roms)
 
    self.led = Pin(27, Pin.OUT)
    self.mqtt_server = 'test.mosquitto.org'
    self.client_id = ubinascii.hexlify(machine.unique_id())
    self.topic_sub = b'notification'
    self.topic_pub = b'hello'

    self.last_message = 0
    self.message_interval = 1 #5. tempo de leitura em segundos. 
    self.counter = 0

  
  def read_ds_sensor(self):
    self.ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in self.roms:
      temp = self.ds_sensor.read_temp(rom)
      if isinstance(temp, float):
        msg = temp #round(temp, 4)
   #    print(temp, end=' ')
   #    print('Valid temperature')
        return msg
    return b'0.0'

  def sub_cb(self):
    return
  
  def connect_and_subscribe(self):
    #global client_id, mqtt_server, topic_sub
    client = MQTTClient(self.client_id, self.mqtt_server)
    #client.set_callback(self.sub_cb)
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
        if (time.time() - self.last_message) > self.message_interval:
          temp = self.read_ds_sensor()
          msg = b'{ counter: %d, temp: %.2f }' % (self.counter,temp)
          print('publicando... ', msg, ' -> ',self.topic_pub)  
          client.publish(self.topic_pub, msg)
          self.last_message = time.time()
          self.counter += 1
      except OSError as e:
        self.restart_and_reconnect()

