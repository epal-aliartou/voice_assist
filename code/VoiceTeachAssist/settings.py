import json
import m_dialog as dlg

def initialize():
    global commands , config
    global full_recognized_text
    global status , return_dict_geniki , first_time
    global mathimata
    
    status={"TYPE":"ΑΡΧΙΚΗ","RESP":"","ΘΕΜΑ":"tipota","ΔΕΙΚΤΗΣ":"","LESSON":"ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ","LIST":""}
    return_dict_geniki={"TYPE":"ΓΕΝΙΚΗ","RESP":"","ΘΕΜΑ":"","ΔΕΙΚΤΗΣ":"","LIST":""}
    full_recognized_text=""
    first_time=True

    with open('settings.json') as f: 
        file_set=json.load(f)
    
    config=file_set["PC"]
    start_command=config["start-command"]+"/"+config["room"]
    commands=[start_command+"/"+cmnd+"/"+i for cmnd,sub_cmnd in config["commands"].items() for i in sub_cmnd] # for cmnd,sub_cmnd in config["commands"].items():
    
    mathimata=file_set["math"] # print (mathimata)
    for key,value in mathimata.items():
        if not (key=="server" or key=="ΤΡΑΠΕΖΑ"):
            value["ΘΕΜΑ"]=value["ΘΕΜΑ 2"]+value["ΘΕΜΑ 4"]
    
    dlg.dialogos=file_set["dialogos"] # print (mathimata)
    for key,value in dlg.dialogos.items():
        value["FUNC"]=getattr(dlg, value["FUNC"])
        if value["LESSON"]!="" :
            value["RETRY"]=int(value["RETRY"])
            value["PATH"]=mathimata[value["LESSON"]]["PATH"] + mathimata['ΤΡΑΠΕΖΑ']
            if value["ΘΕΜΑ"]=="ΘΕΜΑ 2":
                value["LIST"]=mathimata[value["LESSON"]]["ΘΕΜΑ 2"] 
            elif value["ΘΕΜΑ"]=="ΘΕΜΑ 4":
                value["LIST"]=mathimata[value["LESSON"]]["ΘΕΜΑ 4"]
            else:
                value["LIST"]=mathimata[value["LESSON"]]["ΘΕΜΑ"]
# initialize()
    # b_yliko_2=mathimata["ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ"]["ΘΕΜΑ 2"]
    # b_yliko_4=mathimata["ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ"]["ΘΕΜΑ 4"]
    # b_arxes_2=mathimata["ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ"]["ΘΕΜΑ 2"]
    # b_arxes_4=mathimata["ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ"]["ΘΕΜΑ 4"]
    # b_leit_2=mathimata["ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ"]["ΘΕΜΑ 2"]
    # b_leit_4=mathimata["ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ"]["ΘΕΜΑ 4"]
    # g_prog_2=mathimata["ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ"]["ΘΕΜΑ 2"]
    # g_prog_4=mathimata["ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ"]["ΘΕΜΑ 4"]
    # g_plir_2=mathimata["ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ"]["ΘΕΜΑ 2"]
    # g_plir_4=mathimata["ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ"]["ΘΕΜΑ 4"]
    # g_diktya_2=mathimata["ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ"]["ΘΕΜΑ 2"]
    # g_diktya_4=mathimata["ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ"]["ΘΕΜΑ 2"]
    # b_yliko_all=b_yliko_2+b_yliko_4
    # b_arxes_all=b_arxes_2+b_arxes_4
    # b_leit_all=b_leit_2+b_leit_4
    # g_prog_all=g_prog_2+g_prog_4
    # g_plir_all=g_plir_2+g_plir_4
    # g_diktya_all=g_diktya_2+g_diktya_4
    
    # mathimata["ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ"]["ΘΕΜΑ"]=mathimata["ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ"]["ΘΕΜΑ 2"]+mathimata["ΥΛΙΚΟ ΚΑΙ ΔΙΚΤΥΑ"]["ΘΕΜΑ 4"]
    # mathimata["ΑΡΧΕΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ"]["ΘΕΜΑ"]=b_arxes_all
    # mathimata["ΛΕΙΤΟΥΡΓΙΚΑ ΣΥΣΤΗΜΑΤΑ"]["ΘΕΜΑ"]= b_leit_all
    # mathimata["ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ ΥΠΟΛΟΓΙΣΤΩΝ"]["ΘΕΜΑ"]=g_prog_all
    # mathimata["ΠΛΗΡΟΦΟΡΙΑΚΑ ΣΥΣΤΗΜΑΤΑ"]["ΘΕΜΑ"]=g_plir_all
    # mathimata["ΔΙΚΤΥΑ ΥΠΟΛΟΓΙΣΤΩΝ"]["ΘΕΜΑ"]=g_diktya_all


