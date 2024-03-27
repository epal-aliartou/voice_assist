import json
from m_MQTT import *
from  m_PC import go_to_sites_local
import settings as glb2

def func1(msg):             #cmnd/lab1/voice/browse
    msg=msg.decode('UTF-8')
    msg=json.loads(msg)
    print("func1", type(msg), msg)
    go_to_sites_local(msg)

def func2(msg):             #cmnd/lab1/voice/playfile
    msg=msg.decode('UTF-8')
    msg=json.loads(msg)
    print("func2", type(msg), msg)
    

def on_message(client, userdata, msg): # print message, useful for checking if it was successful
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload)) 
    # global commands
    print (glb2.commands)
    for i in range(0,len(glb2.commands)):
        if msg.topic==glb2.commands[i]:
            funcs[i](msg.payload)
            break
    else:
        print("Άγνωστη εντολή με payload=",msg.payload.decode('UTF-8')) 

 
def start_mitsos_agent(test=False):
    client.on_message = on_message
    client.subscribe(glb2.config["start-command"]+"/"+glb2.config["room"]+"/#", qos=1)
    if test: test_browse()
    client.loop_forever()


def test_browse():
    test=["TEST_FILE_URL"]
    test=json.dumps(test)
    client.publish("cmnd/lab1/voice/browse", payload=test, qos=1)

funcs=[func1,func2]


