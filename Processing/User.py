import json
from flickrapi import FlickrAPI
import datetime as dt
flickrKey = "708e1bf66437737bf86c19a4970ee1d9" #queste sono le mie credenziali di FLickr, puoi richiederne altre,
flickrSecret = '6528a8585689bc06'               #oppure usare queste, ma non condividerle con nessuno
client_flickr = FlickrAPI(api_key=flickrKey,secret=flickrSecret,format="parsed-json")

"""Questo file ti consente di ricavare un json con le informazioni degli utenti di FLickr, che hanno visitato
una certa area(bbox), in un certo lasso di tempo(che deciderai tu)"""

"""l'esecuzione può richiedere anche qualche minuto, dipende da quanto sarà grande l'intervallo di tmepo
che indicherai"""

"""ci sono molte diverse funzioni qui definite, ma quando userai il codice dovrai solo richiamare la funzione:
°°°°°user_ifo°°°°°, le altre servono solo a poter eseguire quest'ultima. 
dovrai dare come input le seguenti informazione:

----bbox = le coordinate dell'area che intendi utilizzare(le coordinate devono essere racchiuse tra virgolette "" )
            ti consiglio questo sito per trovare le coordinate http://bboxfinder.com/
---- start_year = l'anno di inizio del cui vuoi conoscere le info
---- start_month = mese d'inizio
---- start_day = giorno d'inizio
---- max_year = anno di fine
---- max_month = mese di fine
---- max_day = giorno di fine
---- path = una stringa racchiusa tra virgolette che indica il percorso in cui vuoi salvare il jason
            esempio: Directory/altra_directory/nome_file.json"""



"""ecco un sempio di come richiamare il codice su un file main e di come usarlo
 
import User as us

user = us.user_info(bbox= bbox, start_year=2019, start_month=6,start_day=1,
                           max_year=2019, max_month=6, max_day=7, path= "File/prova_user.json")

"""

"""NB non tutti gli utenti specificano il proprio luogo di residenza quindi qualche casella location potrebbe essere
vuota"""


def createJson(data:[],path: str):
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def json_extract(obj, key):
    arr = []
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def photosearch( bbox,accuracy,start_year,start_month, start_day, max_year,max_month,max_day, page):
    photos = client_flickr.do_flickr_call(_method_name="flickr.photos.search",
                               bbox = bbox,
                               accuracy=accuracy,
                               content_type=1,
                               min_taken_date = dt.datetime(year=start_year,month=start_month,day=start_day,hour=00,minute=00,second=00),
                               max_taken_date = dt.datetime(year=max_year,month=max_month,day=max_day,hour=23,minute=59,second=59),
                               extras = "date_upload,date_taken,owner_name,geo",
                               per_page = 500,
                               page = page)
    return photos

def num_pages(photo:[]):
    pages = json_extract(photo,"pages")
    num_pages = pages[0]
    return num_pages

def user_info(bbox,start_year,start_month, start_day, max_year,max_month,max_day, path):
    photo = photosearch(bbox=bbox, accuracy=16, start_year=start_year, start_month=start_month,
                        start_day=start_day, max_year=max_year, max_month=max_month, max_day=max_day,
                        page=1)
    pages = num_pages(photo)
    photos = []
    for i in range(1, pages + 1):
        photos.append(photosearch(bbox=bbox, accuracy=16, start_year=start_year, start_month=start_month,
                                  start_day=start_day, max_year=max_year, max_month=max_month, max_day=max_day,
                                  page=i))

    owner = json_extract(photos, "owner")

    owners = list(dict.fromkeys(owner))

    user_info = []
    for x in owners:
        user_info.append(client_flickr.do_flickr_call(_method_name="flickr.people.getInfo", user_id=x))

    createJson(user_info, path)
    return user_info


