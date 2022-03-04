import googlemaps as gmap
import Funzioni.Credenziali as key
client = gmap.Client(key.googleKey)
placeX = []
"""la seguente funzione resituisce un insieme di luoghi(google maps) date delle coordinate"""
def places(location,radius):
    place = gmap.client.places_nearby(client=client, location=location,
                                      radius=radius,type="touristic_attraction",
                                      keyword="touristic,point_of_interest,museum")
    placeX.append(place)
    return placeX

"""ora rifaccio la stessa funzione ma per più luoghi"""
def places_set(foto:[]):
    coordinate = []
    for x in foto:
        coordinate.append([x["lat"], x["long"]])##se non funziona, sostituisci le graffe con le quadre
    for i in range(0, len(coordinate)):
        place = places(coordinate[i], radius=10)
    # di questi elimino le corrispondenze non trovate
    places_n = []
    for x in place:
        if x['status'] != "ZERO_RESULTS":
            places_n.append(x)

    return places_n

#dal dataset ottenuto voglio ekiminare i duplicati
# e di tutte le info prendere in considerazione il nome del luogo, e el coordinate
from Funzioni.JsonFunction import json_extract as ext

def places_info(place_n:[]):
    place_name = ext(place_n, 'name')
    place_name = list(dict.fromkeys(place_name))
    """
    places = []
    for x in place_name:
        place = {"name": x}
        places.append(place)
    """

    #da questo set estraggo le coordinate effettive dei luoghi che mi serviranno per popolare il dataset
    lat = ext(place_n, 'lat')
    latx = []
    i = 0
    while i < len(lat):
        latx.append(lat[i])
        i = i + 3
    latitude = list(dict.fromkeys(latx))

    lng = ext(place_n, 'lng')
    long = []
    i = 0
    while i < len(lng):
        long.append(lng[i])
        i = i + 3
    longitude = list(dict.fromkeys(long))

    coordinate = []
    i = 0
    while i < len(latitude):
        coordinate.append({"name":place_name[i],"lat":latitude[i],"long":longitude[i]})
        i = i + 1
    return coordinate # qui avrò le coordinate effettive dei luoghi, eliminate quelle duplicate
    """ho questo set di coordinate che effettivamente mi servono o per rappresentare i singoli percorsi
    oppure per fare inferenza"""

def place_features (places:[]):
    coordinate = []
    name = []
    luoghi = []
    for x in places:
        coordinate.append({"coordinate": x["results"][0]["geometry"]["location"]})
        name.append({"name": x["results"][0]["name"]})

    for i in range(len(name)):
        luoghi.append({"place": [name[i], coordinate[i]]})
    return luoghi