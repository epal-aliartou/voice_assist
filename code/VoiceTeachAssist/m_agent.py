# from a_globals import *
import json # list = ["1", 2, (3, 4)] # Note that the 3rd element is a tuple (3, 4)# print(x=json.dumps(list)) # '[1, 2, [3, 4]]'#json.dumps(list)# print(x, type(x))
from m_MQTT import *
from  m_PC import go_to_sites_local
import settings as glb2



# commands=[]
# config={}

def func1(msg):             #cmnd/lab1/voice/browse
    msg=msg.decode('UTF-8')
    msg=json.loads(msg)
    
    print("func1", type(msg), msg)
    go_to_sites_local(msg)
    pass

def func2(msg):             #cmnd/lab1/voice/playfile
    msg=msg.decode('UTF-8')
    msg=json.loads(msg)
    print("func2", type(msg), msg)
    pass

def on_message(client, userdata, msg): # print message, useful for checking if it was successful
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload)) # print(type(msg.payload))# # print(b'Easy \xE2\x9C\x85'.decode("utf-8"))# print(msg.payload.decode('UTF-8'))# found=False
    # global commands
    print (glb2.commands)
    for i in range(0,len(glb2.commands)):
        if msg.topic==glb2.commands[i]:
            funcs[i](msg.payload)
            break
    else:
        print("Άγνωστη εντολή με payload=",msg.payload.decode('UTF-8')) 

 
def start_mitsos_agent(test=False):
    # global config
    # global commands
    # config=myconfig
    # commands=mycommands
    client.on_message = on_message
    client.subscribe(glb2.config["start-command"]+"/"+glb2.config["room"]+"/#", qos=1)
    if test: test_browse()
    client.loop_forever()


def test_browse():
    test=["https://eclass.sch.gr/modules/document/file.php/0740110278/B-EPAL-PYTHON/TRAPEZA/16275_SOLUTION.pdf","https://eclass.sch.gr/modules/document/file.php/0740110278/B-EPAL-PYTHON/TRAPEZA/16275.pdf"]
    test=json.dumps(test)
    client.publish("cmnd/lab1/voice/browse", payload=test, qos=1)

funcs=[func1,func2]

# funcs=[func1,func2] #print(commands)  #1- cmnd/lab1/voice/browse #2- cmnd/lab1/voice/playfile
# test_browse()
# client.on_publish = on_publish


