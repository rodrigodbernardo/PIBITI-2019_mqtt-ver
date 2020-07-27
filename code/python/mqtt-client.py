'''
Cliente MQTT para Python
Autor: Rodrigo D B Araujo


'''

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc): 
    if(rc==0):
        print("Connected!")
    else:
        print("Bad connection. Return code = ",rc)
   #reconectar aqui
   #client.subscribe("blabla")

def on_message(client, userdata, message): 
   #if str(message.topic) != pubtop: 
    print(str(message.topic) + " " + str(message.payload))

def on_subscribe(client, userdata, mid, granted_qos): 
   print("Subscribed:" + str(mid) + str(granted_qos)) 
def on_unsubscribe(client, userdata, mid): 
   print("Unsubscribed:" + str(mid)) 
def on_disconnect(client, userdata, rc): 
   if rc != 0: 
       print("Unexpected disconnection.") 
def on_log(client,userdata,level,buf):
    print("log: " + buf)

#broker_address = "iot.eclipse.org" 
#port = 1883 
broker_address = "broker.hivemq.com"
#port = 8000

client = mqtt.Client("rdba_pyclient") 
client.on_subscribe = on_subscribe 
client.on_unsubscribe = on_unsubscribe 
client.on_connect = on_connect 
client.on_message = on_message 
client.on_log = on_log
time.sleep(1) # Sleep for a beat to ensure things occur in order 
client.connect(broker_address) 

#client.loop_forever()
#pubtop = input('Publish topic: ') 
#subtop = input('Subscribe topic: ') 

client.loop_start() 
client.subscribe("rdba/topico_02")
# Updated chat loop 
while True: 
    chat = input() 
    client.publish("rdba/topico_01", chat) 
# Disconnect and stop the loop! 
time.sleep(5)
client.disconnect() 

client.loop_stop() 
