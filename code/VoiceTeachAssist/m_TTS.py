from gtts import gTTS
from playsound import playsound
import os
import settings as glb
from termcolor import colored

# print("...........................")
# playsound("Audio/beep-027.mp3",True)

# print (colored('hello', 'red'), colored('world', 'yellow'))
def Print_dont_talk(text, mycolor="white"):
    print (colored(text, mycolor))

def mitsos_talk(text,mycolor="green"):                      # convert text to speech
    if glb.config["local_talk"]:
        file_name = "audiodata.mp3"     #1 file_name =text+str(random.randint(100, 999))+".mp3"
        tts = gTTS(text=text, lang='el')# convert text to speech
        tts.save(file_name)             # save file      
        playsound(file_name)            # play file
        os.remove(file_name)            #2 remove file
    else:
        Print_dont_talk(text, mycolor)

# Print_dont_talk("tttttttttttttt")
# Print_dont_talk("tttttttttttttt","red")
# Print_dont_talk("tttttttttttttt")
# Print_dont_talk("tttttttttttttt","green")


