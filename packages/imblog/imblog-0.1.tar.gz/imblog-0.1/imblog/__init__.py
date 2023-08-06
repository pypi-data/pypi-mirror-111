import time,os
from imblog.common import config, utils, Requests
import requests
from imblog.Client import Client
def start():
    try:
        utils.clear_data()
        lst_objs = requests.get(config.ServerAdress.BLOG_SERVER + "client/get").json()
        lst_clients = []
        for obj in lst_objs:
            client = Client(obj['id'], obj['email'], obj['album_id'], config.Timeout.THREAD)
            client.start()
            lst_clients.append(client)
            time.sleep(60)
        for client in lst_clients:
            client.wait()
        print('done')
    except:
        pass
    os.system("reboot")
