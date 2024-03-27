import speech_recognition as sr
import unicodedata as ud
import settings as glb
from termcolor import colored

# recognized_text=""


def mitsos_listen():                        # convert speech to text so we can use the text for the next step
    if glb.config["local_listen"]:
        r = sr.Recognizer()                     # create recognizer # global recognized_text
        with sr.Microphone() as source:         # what we speak into the microphone should be our source
            audio = r.listen(source)            # use the listen function so the recognizer can cathch the source (our mic)
            text = ''
            try:
                text = r.recognize_google(audio , language="el") 
            except sr.RequestError as re:
                print(re)
            except sr.UnknownValueError as uve:
                print(uve)
            except sr.WaitTimeoutError as wte:
                print(wte)
        text = text.lower()
        if text!= "":
            print(colored("Recognized ="+text, "yellow"))
        else:
            print(colored("Σιωπή.......", "red"))
    else:
        # text = input()
        text =  input(colored('Πές μου: ', 'red','on_yellow')+'?: ')
    text=ud.normalize('NFD',text).upper().translate( {ord('\N{COMBINING ACUTE ACCENT}'):None})
    glb.full_recognized_text=text     # recognized_text=text
    return text
    