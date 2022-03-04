from Funzioni import GmapFunction as gmap
from Funzioni import JsonFunction as jf

def mostVisisted(photo:[], placesNumber:int):
    photon = []

    for x in photo:
        coordinate = []
        for i in range(0, len(x[1])):
            coordinate.append(x[1][i]["coordinate"])
        photon.append({x[0]: list(dict.fromkeys(coordinate))})
    new_coordinate = []
    from collections import Counter
    for x in photon:
        for i in range(0, len(list(x.values())[0])):
            new_coordinate.append(list(x.values())[0][i])

    counter = Counter(new_coordinate)
    c = counter.most_common(placesNumber)
    place = []

    for i in range(0, len(c)):
        place.append(gmap.places(location=c[i][0], radius=20))
    jf.createJson(place,"File/FileOriginali/places.json")
    info_place = gmap.places_info(place)
    jf.createJson(info_place,"File/place.json")
    jf.createJson(c, "File/MostVisited.json")
    return info_place,c
    #c contiente le statistiche, infor:place contiene i luoghi di interesse ricavati da google


