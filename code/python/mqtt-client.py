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
   
    #a inscricao feita aqui garante que o cliente irá se reconectar caso a rede caia e volte depois
    client.subscribe(outTopic)

def on_message(client, userdata, message): 
    print(str(message.topic) + " " + message.payload.decode("utf-8"))

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
broker_addr = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("rdba_pyclient001") 
client.on_subscribe = on_subscribe 
client.on_unsubscribe = on_unsubscribe 
client.on_connect = on_connect 
client.on_message = on_message 
#client.on_log = on_log
time.sleep(1) # Sleep for a beat to ensure things occur in order 
client.connect(broker_addr) 

'''
outTopic --> Do sensor para o computador
inTopic  --> Do computador para o sensor
'''

outTopic = "rdba/outTopic"
inTopic  = "rdba/inTopic"

client.loop_start()
time.sleep(5)

while True: 
    print('What do you want to do?')
    print('1-Data capture')
    print('2-Live View')
    print('3-Exit')

    menu = input('\n>>> ')

    if(menu == "1"):
        cmd = "cmd_capt"
        nCapture = int(input("Number of Captures: "))
        nSample  = int(input("Number of Samples: "))
        sampleRate = int(input("Sample rate(ms): "))
    elif(menu == '2'):
        cmd = "cmd_live"
        nCapture = 0
        nSample  = 0
        sampleRate = int(input("Sample rate(ms): "))
    elif(menu == '3'):
        break

    else:
        print('Unknown command. Try again.\n\n')
        continue
    data = "{\"cmd\":\""+ str(cmd) + "\",\"nCapture\":" + str(nCapture) + ",\"nSample\":" + str(nSample) + ",\"sampleRate\":" + str(sampleRate) + "}"
    print(data)
    client.publish(inTopic, data) 

client.disconnect() 
client.loop_stop() 
