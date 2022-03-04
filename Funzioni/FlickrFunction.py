import time
import datetime as dt

from flickrapi import FlickrAPI
import Funzioni.Credenziali as key
import json
import Funzioni.JsonFunction as js
client_flickr = FlickrAPI(api_key=key.flickrKey,secret=key.flickrSecret,format="parsed-json")
bbox = "12.343140,41.796729,12.625122,42.000419"

"""questa funzione consente di interrogare flickr e di ricevere le foto
-input: coordinate della bbox(cioè un'area rettangolare che delimita la regione di ricerca),
        acuratezza della ricerca valori di ingresso(16,11,7,3 specificano la precisione),
         data inizio,
         data fine,
         numero pagina"""
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

"""la prossima funzione deve dividere le foto per proprietario"""

def perOwner(photo:[]):
    owner = []
    for x in photo:
        owner.append(x["owner"])## mi segno ogni singolo proprietario

    #elimino i duplicati
    from collections import OrderedDict
    single_owner = OrderedDict((x, True) for x in owner).keys()
    owner = list(single_owner)
    ### divido le foto per proprietario
    user = []
    phots_for_owner = []
    for i in range(0, len(owner)):
        for j in range(0, len(photo)):
            if photo[j]["owner"] == owner[i]:
                phots_for_owner.append(photo[j])

    return perOwner(phots_for_owner)



        #mi creo così un file contente le foto dei singoli utenti,ma effettivamente sta cosa mi serve?
        #in realtà potrenìbbe servirmi per le statistiche, ma per adesso la lascio, di fatti ciò che mi
        #serve adesso è usare tutto il dataset unito




"""la prossima funzione mi consente di prendere solo le informazioni che mi servono dal dataset di flickr
-input: dataset delle foto"""

def features(photos:[],num_pages):
    set = []
    for i in range(0,num_pages):
        data = photos[i]["photos"]["photo"]  ##le foto sono così annidate nel json di flickr

        for x in data:
            set.append({"date":x["datetaken"],"owner":x["owner"] ,"coordinate":str(x["latitude"][0:6])+","+str(x["longitude"][0:6])})

    """ricavo coordinate, proprietario e data"""

    return set


"""la seguente funzione mi consente di riordinare il tutto in base alla data"""

def date(set:[]):
    date = []
    ###questo codice mi modifica la data in unique epoch time

    for x in set:
        date.append({"date":time.mktime(dt.datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S").timetuple()),
                     "owner":x["owner"],"coordinate":x["coordinate"]})

    sorted_json_data = sorted(date, key=lambda x: x['date'])
    return sorted_json_data


import Funzioni.JsonFunction as jf
def num_pages(photo:[]):
    pages = jf.json_extract(photo,"pages")
    num_pages = pages[0]
    return num_pages


