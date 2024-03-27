import webbrowser
import time
import json
from m_MQTT import client
import settings as glb


def go_to_sites_local(sites):
    for site in sites:
        webbrowser.open(site)
        time.sleep(0.5)

def go_to_sites(sites):
    if glb.config["i_am_server"]:
        if glb.config["remote_command"]:
            str_sites=json.dumps(sites)
            client.publish(glb.commands[0], payload=str_sites, qos=1)
        if glb.config["local_command"]:
            go_to_sites_local(sites)

# webbrowser.open("file:///C:/0-%CE%98%CE%95%CE%9C%CE%91%CE%A4%CE%91/%CE%93%20%CE%95%CE%A0%CE%91%CE%9B%20%CE%94%CE%99%CE%9A%CE%A4%CE%A5%CE%91%20%CE%9A%CE%95%CE%A64%20%CE%A4%CE%A1%CE%91%CE%A0%CE%95%CE%96%CE%91%20%CE%9F%CE%9B%CE%91.pdf")