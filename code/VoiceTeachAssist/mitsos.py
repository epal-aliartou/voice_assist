import settings as glb
import m_dialog as dlg #import dialogos,find_keys_in_recognition,find_thema_everywhere,is_5_digit,initialize_var_dialogos
from  m_TTS import mitsos_talk
from  m_STT import mitsos_listen
from  m_agent import client,mqtt,start_mitsos_agent
from  termcolor import colored

def get_variable_name(var):                      
    for name, value in globals().items():
        if value is var:
            return name
    return None

def mitsos_first_question(question):
    mitsos_talk(question)
    listened = mitsos_listen()
    listened= " ΜΑΘΗΜΑ"+listened
    glb.first_time=False
    return listened

def mitsos_other_question(question):
    mitsos_talk(question)
    listened = mitsos_listen()
    is_5_d, listened =dlg.is_5_digit(listened)
    if is_5_d:
        d=dlg.find_thema_everywhere(listened)
        if d is not None: 
            glb.status=d
    return listened

def start_mitsos_dialog():
    # global status # initialize_var(config,commands) # first_time=True
    while True:
        if glb.first_time:
            what_mitsos_listened=mitsos_first_question("Πες ΜΑΘΗΜΑ,  και μετά το μάθημα που έχεις.")
        else:
            what_mitsos_listened=mitsos_other_question("Άλλη ερώτηση;")
        for key,dialog in dlg.dialogos.items():
            if dlg.find_keys_in_recognition(dialog["REC"],what_mitsos_listened):
                # print("προτου θεμα=" , status["ΘΕΜΑ"])
                print(colored(f'ΠΡΟΤΟΥ ΕΝΤΟΛΗ={key} ΘΕΜΑ={str(glb.status["ΘΕΜΑ"])},ΔΕΙΚΤΗΣ={str(glb.status["ΔΕΙΚΤΗΣ"])},LESSON={str(glb.status["LESSON"])} ,ΘΕΜΑΤΑ ΣΤΗ ΛΙΣΤΑ={len(glb.status["LIST"])}',"light_magenta"))
                if dialog["TYPE"]=="ΣΥΝΕΧΕΙΑ":
                    glb.status["RESP"]=dialog["RESP"]
                    dialog["FUNC"](glb.status,key)
                elif dialog["TYPE"]=="ΓΕΝΙΚΗ":
                    dialog["FUNC"](dialog)
                else :
                    glb.status=dialog["FUNC"](dialog)
                print(colored(f'ΜΕΤΑ ΕΝΤΟΛΗ={key} ΘΕΜΑ={str(glb.status["ΘΕΜΑ"])},ΔΕΙΚΤΗΣ={str(glb.status["ΔΕΙΚΤΗΣ"])},LESSON={str(glb.status["LESSON"])} ,ΘΕΜΑΤΑ ΣΤΗ ΛΙΣΤΑ={len(glb.status["LIST"])}',"light_magenta"))
                break

def connect_to_mqtt():
    client.username_pw_set(glb.config["mqtt-user"], glb.config["mqtt-pwd"])
    if glb.config["mqtt-remote"]: 
         client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS) # enable TLS for secure connection
    client.connect(glb.config["mqtt-server"], glb.config["mqtt-port"])

def write_dict2CSV(myDict,myFile='mycsvfile1.csv'):
    import csv
    with open(myFile, 'w') as f:  
        w = csv.DictWriter(f, myDict.keys())
        w.writeheader()
        w.writerow(myDict)

def write_dict_of_dict_to_CSV(myDict):
    import csv
    with open('AllDict.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
        for key,value in myDict.items():
            w = csv.DictWriter(f, value.keys())
            f.write(key+"\n")
            w.writeheader()
            w.writerow(value)        
      
def write_dict_of_dict_to_CSVS(myDict):
    i=0
    for key,value in myDict.items():
        i+=1
        write_dict2CSV(value,str(i)+"-"+key+".csv")
 
def start_Dialog_or_Agent():
    dlg.initialize_var_dialogos()
    glb.initialize() # get_config_from_file() #print ("START===", commands,"START===", config) 
    if glb.config["i_am_server"]:
        if glb.config["remote_talk"] or glb.config["remote_command"] :connect_to_mqtt()
        start_mitsos_dialog()
    else:
        connect_to_mqtt()
        start_mitsos_agent( test=False)

if __name__ == "__main__":
    start_Dialog_or_Agent()
    

