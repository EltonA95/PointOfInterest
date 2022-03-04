from functools import partial
from itertools import groupby
import itertools
from operator import itemgetter
import Funzioni.FlickrFunction as ff
import Funzioni.JsonFunction as jf
from operator import itemgetter
"""mi definisco una funzione che mi restituisce l'array finale delle foto, con le informazioni che mi servono,
 raggruppate per singolo utente"""
def del_ret(d, key):
    del d[key]
    return d
def photoProcessing(bbox,  start_year, start_month, start_day, max_year, max_month, max_day,accuracy=16):
        photo = []
        photo = ff.photosearch(bbox=bbox,accuracy=accuracy,start_year=start_year,start_month=start_month,
                               start_day=start_day,max_year=max_year,max_month=max_month,max_day=max_day,
                               page=1)
        photos = []
        num_pages = ff.num_pages(photo)
        for i in range(1,num_pages+1):
            photos.append(ff.photosearch(bbox=bbox,accuracy=accuracy,start_year=start_year,start_month=start_month,
                               start_day=start_day,max_year=max_year,max_month=max_month,max_day=max_day,
                               page=i))
        jf.createJson(photos,"File/FileOriginali/photos.json")

        features = ff.features(photos,num_pages=num_pages)
        featuresx = ff.date(features)
        #devo raggruppare tutto per proprietario
        per_user = featuresx.sort(key=lambda x:x["owner"])
        per_user = dict(map(lambda k_v: (k_v[0], tuple(map(partial(del_ret, key="owner"), k_v[1]))),
                            groupby(featuresx, itemgetter("owner"))))
        """questo codice mi serve pe raccedere agli elemnti"""
        new_list = []
        for key, val in per_user.items():
            new_list.append([key, val])
        jf.createJson(new_list, "File/FlickrPhotos.json")
        return new_list
"""la funzione sopra mi restituisce un array e se voglio lo stampo anche in un json"""

