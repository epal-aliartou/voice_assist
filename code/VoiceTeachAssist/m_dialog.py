
import datetime # from babel.dates import format_datetime
import random
import re
from  m_TTS import mitsos_talk,os
from  m_STT import mitsos_listen
from  m_PC import go_to_sites
import settings as glb # from  m_trapeza import *
import locale          # from a_globals import *

# print (paths['server']+paths[status["LESSON"]]+"BIBLIO.PDF" )
# webbrowser.open("https://eclass.sch.gr/modules/document/file.php/0740110278/G-EPAL-DIKTYA/BIBLIO.pdf")
# print (str([int(i) for i in "full 11 recognized_text 33".split() if i.isdigit()]))
# glb.initialize()
# glb.config["local_talk"]=True
# mitsos_talk(datetime.datetime.now().strftime("%H:%M %p"))
# print (datetime.datetime.now().strftime("%H:%M %p"))
# print (datetime.datetime.now().strftime("%A %d %B %Y"))
# mathimata=glb.mathimata

def replace_all(repls, str):                                 
    return re.sub('|'.join(re.escape(key) for key in repls.keys()),  # return re.sub('|'.join(repls.keys()), lambda k: repls[k.group(0)], str)    
                  lambda k: repls[k.group(0)], str) 
                                                                    # text =  "i like apples, but pears scare me" # print replace_all({"apple": "pear", "pear": "apple"}, text)                                    

def month_replace(mydate):
    replacers = {'Ιανουάριος ':'Ιανουαρίου' , 'Φεβρουάριος' :'Φεβρουαρίου' , 'Μάρτιος' :'Μαρτίου' ,'Απρίλιος' :'Απριλίου' ,'Μάιος':'Μαΐου' , 'Ιούνιος':'Ιουνίου','Ιούλιος':'Ιουλίου','Αύγουστος':'Αυγούστου','Σεπτέμβριος':'Σεπτεμβρίου','Οκτώβριος':'Οκτωβρίου','Νοέμβριος':'Νοεμβρίου','Δεκέμβριος':'Δεκεμβρίου'} #etc....
    return  replace_all(replacers, mydate) # text =  "25 Μάρτιος  Ιανουάριος  Φεβρουάριος  Απρίλιος 2024" text =datetime.datetime.now().strftime("%A %d %B %Y")

def time_now(my_dict):
    # time_now=format_datetime(datetime.datetime.now(), "H:mm a", locale='el')
    locale.setlocale(locale.LC_TIME, 'el_GR.UTF-8')
    time_now = datetime.datetime.now().strftime("%H:%M %p")
    mitsos_talk(my_dict["RESP"]+ time_now)
    return glb.return_dict_geniki

def weekday_now(my_dict):
    # weekday_today=format_datetime(datetime.datetime.now(), "medium", locale='el') #"EEEE"
    # mitsos_talk(my_dict["RESP"] + weekday_today)
    locale.setlocale(locale.LC_TIME, 'el_GR.UTF-8')
    mitsos_talk(my_dict["RESP"] + month_replace(datetime.datetime.now().strftime("%A %d %B %Y")))
    return glb.return_dict_geniki
    
def break_now(my_dict):
    mitsos_talk(my_dict["RESP"])
    os._exit(1)
    return return_dict_geniki

def find_thema_once(my_dict1,anaggelia,prothema=""):
    mitsos_talk (prothema+anaggelia)        
    thema = mitsos_listen()
    if find_keys_in_recognition(dialogos["ΤΥΧΑΙΟ"]["REC"],thema):
        thema =random.choice(my_dict1["LIST"])
    else :
        thema=thema.replace(" ", "")
    if thema in my_dict1["LIST"]:
        go_to_sites([glb.mathimata['server']+my_dict1["PATH"]+thema+".pdf",glb.mathimata['server']+my_dict1["PATH"]+thema+"_SOLUTION.pdf" ])
        # print (my_dict1)
        my_dict1=my_dict1 | {"ΘΕΜΑ":thema, "ΔΕΙΚΤΗΣ":my_dict1["LIST"].index(thema)}
        # print (my_dict1)
        return True , my_dict1
    else:
        return False, my_dict1

def find_thema(my_dict):
    found,my_dict =find_thema_once(my_dict, my_dict["RESP"])                 
    if found: 
        return my_dict        
    else :
        i=0
        while i<my_dict["RETRY"] :
            found,my_dict =find_thema_once(my_dict, my_dict["RESP"])                 
            if found: return my_dict
            i+=1
        else:
            mitsos_talk ("Δεν μπόρεσα να καταλάβω το θεμα που θέλεις.Σε πάω στο πρώτο θέμα της λίστας.")
            go_to_sites([glb.mathimata['server']+my_dict["PATH"]+my_dict["LIST"][0]+".pdf",glb.mathimata['server']+my_dict["PATH"]+my_dict["LIST"][0]+"_SOLUTION.pdf" ])
            return my_dict | {"ΘΕΜΑ":my_dict["LIST"][0], "ΔΕΙΚΤΗΣ":0}

def next_thema(status, *args):
    if status["ΔΕΙΚΤΗΣ"]=="" :
        mitsos_talk ("Δεν έχει επιλεγεί μάθημα.")
        return
    if int(status["ΔΕΙΚΤΗΣ"])<len(status["LIST"]):
        mitsos_talk (status["RESP"])
        status["ΔΕΙΚΤΗΣ"]=int(status["ΔΕΙΚΤΗΣ"])+1
        status["ΘΕΜΑ"]=status["LIST"][int(status["ΔΕΙΚΤΗΣ"])]
        go_to_sites([glb.mathimata['server']+status["PATH"]+status["ΘΕΜΑ"]+".pdf",glb.mathimata['server']+status["PATH"]+status["ΘΕΜΑ"]+"_SOLUTION.pdf" ])
        return

def find_lesson_book(status,*args):
    # global full_recognized_text
    found=False
    for key,value in glb.mathimata.items():
        if not (key=="server" or key=="ΤΡΑΠΕΖΑ"):
            if find_keys_in_recognition(value["REC"],glb.full_recognized_text):
                find_book(status, new_book=value ["PATH"])
                found=True
                break
    if not found : find_book(status)
    return

def find_book(status, new_book=""):
    # test_str=""
    # global full_recognized_text
    if status["LESSON"] =="" and new_book == "":
        mitsos_talk ("Δεν έχει επιλεγεί μάθημα.")
        return
    else:
        number_in_responce=find_number_in_responce(glb.full_recognized_text)
        biblio="BIBLIO.pdf"
        if number_in_responce != []:
            biblio=biblio+ "#page=" + str(number_in_responce[0]+1)
        if new_book != "":
            url=glb.mathimata['server']+new_book+ biblio
        else:
            url=glb.mathimata['server']+glb.mathimata[status["LESSON"]]["PATH"] + biblio
        mitsos_talk (status["RESP"])
        go_to_sites([url])
    
def find_number_in_responce(mystr):
    # print ("find_number_in_responce=", mystr)
    return [int(i) for i in mystr.split() if i.isdigit()]

def random_thema(status,*args):
    if status["LIST"] =="" :
        mitsos_talk ("Δεν έχει επιλεγεί μάθημα.")
    else:
        mitsos_talk (status["RESP"])
        status["ΘΕΜΑ"]=random.choice(status["LIST"])
        status["ΔΕΙΚΤΗΣ"]=status["LIST"].index(status["ΘΕΜΑ"])
        go_to_sites([glb.mathimata['server']+status["PATH"]+status["ΘΕΜΑ"]+".pdf",glb.mathimata['server']+status["PATH"]+status["ΘΕΜΑ"]+"_SOLUTION.pdf" ])
    return

def find_keys_in_recognition (regex,listen):
    # https://blog.finxter.com/python-regex-and-operator-tutorial-video/
    # global full_recognized_text
    # glb.full_recognized_text=listen
    return re.search(regex,listen) 

def find_mathima(mydict):
    # global full_recognized_text
    found=False
    for key,value in glb.mathimata.items():
        if not (key=="server" or key=="ΤΡΑΠΕΖΑ"):
            if find_keys_in_recognition(value["REC"],glb.full_recognized_text):
                mydict=mydict | {"PATH":value ["PATH"]+ glb.mathimata["ΤΡΑΠΕΖΑ"],"LESSON":key,"ΔΕΙΚΤΗΣ":"0","LIST":value ["ΘΕΜΑ"],"ΘΕΜΑ":value ["ΘΕΜΑ"][0]}
                find_book(mydict, new_book=value ["PATH"])
                found=True
                break
    if not found : find_book(mydict)
    return mydict

def find_thema_everywhere(resp_5_d):
    d={"PATH":"","TYPE":"ΜΑΘΗΜΑ","RESP":"","ΘΕΜΑ":"tipota","ΔΕΙΚΤΗΣ":"","LESSON":"ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ","LIST":""}
    # global full_recognized_text
    found=False
    for key,value in glb.mathimata.items():
        if not (key=="server" or key=="ΤΡΑΠΕΖΑ"):
            for thema in value["ΘΕΜΑ 2"]:
                if thema==resp_5_d:
                    d["LIST"]=value["ΘΕΜΑ 2"]
                    d["ΘΕΜΑ"]=resp_5_d
                    d["ΔΕΙΚΤΗΣ"]=value["ΘΕΜΑ 2"].index(resp_5_d)
                    d["LESSON"]=key
                    d["PATH"]=value["PATH"]+glb.mathimata["ΤΡΑΠΕΖΑ"]
                    d["RESP"]="To θέμα 2 με αριθμό " + resp_5_d +" υπάρχει , στο μάθημα " + d["LESSON"]
                    go_to_sites([glb.mathimata['server']+d["PATH"]+d["ΘΕΜΑ"]+".pdf",glb.mathimata['server']+d["PATH"]+d["ΘΕΜΑ"]+"_SOLUTION.pdf" ])
                    # print (d)
                    mitsos_talk(d["RESP"])
                    return d
            for thema in value["ΘΕΜΑ 4"]:
                if thema==resp_5_d:
                    d["LIST"]=value["ΘΕΜΑ 4"]
                    d["ΘΕΜΑ"]=resp_5_d
                    d["ΔΕΙΚΤΗΣ"]=value["ΘΕΜΑ 4"].index(resp_5_d)
                    d["LESSON"]=key
                    d["PATH"]=value["PATH"]+glb.mathimata["ΤΡΑΠΕΖΑ"]
                    d["RESP"]="To θέμα 4 με αριθμό " + resp_5_d +" υπάρχει , στο μάθημα " + d["LESSON"]
                    go_to_sites([glb.mathimata['server']+d["PATH"]+d["ΘΕΜΑ"]+".pdf",glb.mathimata['server']+d["PATH"]+d["ΘΕΜΑ"]+"_SOLUTION.pdf" ])                    
                    # print (d)
                    mitsos_talk(d["RESP"])
                    return d

def is_5_digit(listened):
    listened_temp=listened.replace(" ", "")
    if listened_temp.isdigit() and len(listened_temp)==5:
        return True,listened_temp
    else:
        return False,listened

def change_list(status, *args):
     status["LIST"]=glb.mathimata[status["LESSON"]][args[0]]
     status["ΘΕΜΑ"]=glb.mathimata[status["LESSON"]][args[0]][0]
     status["ΔΕΙΚΤΗΣ"]=0
     go_to_sites([glb.mathimata['server']+status["PATH"]+status["ΘΕΜΑ"]+".pdf",glb.mathimata['server']+status["PATH"]+status["ΘΕΜΑ"]+"_SOLUTION.pdf" ])

def initialize_var_dialogos(): #def initialize_var_dialogos(myconfig,mycommands):
    # global config #global commands #config=myconfig #commands=mycommands
    global dialogos
    dialogos={}
#     dialogos={
#     "ΗΜΕΡΟΜΗΝΙΑ":{
#     "TYPE":"ΓΕΝΙΚΗ" ,
#     "REC":'ΗΜΕΡΑ|ΗΜΕΡΟΜΗΝΙΑ|ΜΕΡΑ|ΜΗΝΑΣ|ΜΗΝΑ',
#     "RESP":'Σήμερα είναι ',"FUNC":weekday_now,
#     },
#     "ΩΡΑ":{
#     "TYPE":"ΓΕΝΙΚΗ" ,
#     "REC":'ΩΡΑ',
#     "RESP":'Η ώρα είναι ',"FUNC":time_now,
#     },
#     "ΕΞΟΔΟΣ":{
#     "TYPE":"ΓΕΝΙΚΗ",
#     "REC":'ΤΕΡΜΑ|ΒΑΡΕΘΗΚΑ|ΣΤΟΠ|ΣΤΑΜΑΤΑ|ΤΕΛΕΙΩΣΕ|stop',
#     "RESP":'Γειά σου Κούκλε!',"FUNC":break_now
#     },    
#     "ΕΠΟΜΕΝΟ":{
#     "TYPE":"ΣΥΝΕΧΕΙΑ",
#     "REC":'ΕΠΟΜΕΝΟ|ΠΡΟΧΩΡΑ',
#     "RESP":'Ορίστε, το επόμενο Θέμα.',"FUNC":next_thema,
#     },
#     "ΤΥΧΑΙΟ":{
#     "TYPE":"ΣΥΝΕΧΕΙΑ",
#     "REC":'ΤΥΧΑΙΟ|ΤΥΧΗ|ΤΥΧΑΙΑ|ΤΕΣΤ',
#     "RESP":'Καλή Τύχη!Λύσε το τυχαίο Θέμα!',"FUNC":random_thema,
#     },
#     "ΒΙΒΛΙΟ":{
#     "TYPE":"ΣΥΝΕΧΕΙΑ",
#     "REC":'ΒΙΒΛΙΟ|ΤΕΤΡΑΔΙΟ',
#     "RESP":'Ορίστε, το βιβλίο του μαθήματος',"FUNC":find_lesson_book,
#     },
#     "ΘΕΜΑ2_dikt":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))(?=.*(ΔΙΚΤΥΑ|ΔΙΚΤΥΟ|ΔΙΧΤΥ|ΔΙΚΤΥΟ|ΔΙΚ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 2"]
#     },
#     "ΘΕΜΑ4_dikt":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))(?=.*(ΔΙΚΤΥΑ|ΔΙΚΤΥΟ|ΔΙΧΤΥ|ΔΙΚΤΥΟ|ΔΙΚ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ_dikt":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΔΙΚΤΥΑ|ΔΙΚΤΥΟ|ΔΙΧΤΥ|ΔΙΚΤΥΟ|ΔΙΚ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["PATH"] +glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 2"]+glb.mathimata['ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ2_prog":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))(?=.*(ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 2"]
#     },
#     "ΘΕΜΑ4_prog":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))(?=.*(ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ_prog":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 2"]+glb.mathimata['ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ']["ΘΕΜΑ 4"]
#     }, 
#     "ΘΕΜΑ2_plir":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))(?=.*(ΠΛΗΡΟΦΟΡΙΑΚΑ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 2"]
#     },
#     "ΘΕΜΑ4_plir":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"","REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))(?=.*(ΠΛΗΡΟΦΟΡΙΑΚΑ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ_plir":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΠΛΗΡΟΦΟΡΙΑΚΑ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 2"]+glb.mathimata['ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ2_arxes":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))(?=.*(ΑΡΧΕΣ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["ΘΕΜΑ 2"]
#     },
#     "ΘΕΜΑ4_arxes":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))(?=.*(ΑΡΧΕΣ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ_arxes":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#      "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΑΡΧΕΣ))',
#      "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#      "PATH":glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#      "LIST":glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["ΘΕΜΑ 2"]+glb.mathimata['ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ']["ΘΕΜΑ 4"]
#      },
#     "ΘΕΜΑ2_leit":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))(?=.*(ΛΕΙΤΟΥΡΓΙΚΑ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 2"]
#     },
#     "ΘΕΜΑ4_leit":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))(?=.*(ΛΕΙΤΟΥΡΓΙΚΑ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 4"]
#     },
#     "ΘΕΜΑ_leit":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΛΕΙΤΟΥΡΓΙΚΑ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 2"]+glb.mathimata['ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ']["ΘΕΜΑ 4"]
#     }, 
#     "ΘΕΜΑ2_yliko":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#      "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))(?=.*(ΥΛΙΚΟ))',
#      "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#      "PATH":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#      "LIST":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["ΘΕΜΑ 2"]
#      },
#     "ΘΕΜΑ4_yliko":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))(?=.*(ΥΛΙΚΟ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["ΘΕΜΑ 4"]
#      },
#     "ΘΕΜΑ_yliko":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'(?=.*ΤΡΑΠΕΖΑ)(?=.*(ΥΛΙΚΟ))',
#     "RESP":'Ποιό θέμα απο την Τράπεζα θεμάτων θέλεις;',
#     "PATH":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_thema,
#     "LIST":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["ΘΕΜΑ 2"]+glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["ΘΕΜΑ 4"]
#     } ,
#     "ΜΑΘΗΜΑ":{
#     "TYPE":"ΜΑΘΗΜΑ","LESSON":"ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ","RETRY":3,"ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"",
#     "REC":'ΜΑΘΗΜΑ|ΜΑΘΗΜΑΤΟΣ',
#     "RESP":'Μπήκα στο μάθημα.',
#     "PATH":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["PATH"] + glb.mathimata['ΤΡΑΠΕΖΑ'],"FUNC":find_mathima,
#     "LIST":glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["ΘΕΜΑ 2"]+glb.mathimata['ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ']["ΘΕΜΑ 4"]
#     } ,
#     "ΘΕΜΑ 2":{
#     "TYPE":"ΣΥΝΕΧΕΙΑ",
#     "REC":'(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(2|ΔΥΟ))',
#     "RESP":'Άλλαξα την λίστα θεμάτων μόνο σε θέμα 2!',"FUNC":change_list,
#     },
#     "ΘΕΜΑ 4":{
#     "TYPE":"ΣΥΝΕΧΕΙΑ",
#     "REC":'(?=.*(ΘΕΜΑ|ΘΕΑ))(?=.*(4|ΤΕΣΣΕΡΑ))',
#     "RESP":'Άλλαξα την λίστα θεμάτων μόνο σε θέμα 2!',"FUNC":change_list,
#     },
#     "ΘΕΜΑ":{
#     "TYPE":"ΣΥΝΕΧΕΙΑ",
#     "REC":'(?=.*ΘΕΜΑΤΑ)(?=.*(ΟΛΑ|ΠΑΝΤΑ))',
#     "RESP":'Άλλαξα την λίστα θεμάτων μόνο σε όλα τα θέματα!',"FUNC":change_list,
#     },
#     # "5-digits":{
#     # "TYPE":"ΣΥΝΕΧΕΙΑ",
#     # "REC":'^\d{5}$',
#     # "RESP":'Ορίστε, το επόμενο Θέμα.',"FUNC":next_thema,
#     # },
# }

