import requests
from imblog.common import config


def get(path,retries=3):
    e=0
    rs= None
    while e < retries:
        try:
            rs = requests.get(path).text
            break
        except:
            e += 1
            pass
    return rs
def log(id, log):
    path = config.ServerAdress.BLOG_SERVER + "client/log"
    json={
        "id":id,
        "log":log
    }
    rs=requests.post(path, json=json).text
    print(rs)
def update_album_id(id, album_id):
    path = config.ServerAdress.BLOG_SERVER + "client/album/update"
    json = {
        "id": id,
        "album_id": album_id
    }
    rs = requests.post(path, json=json).text
    print(rs)