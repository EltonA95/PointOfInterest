import Funzioni.Credenziali as key
googleKey = key.googleKey
import Funzioni.JsonFunction as jf
import gmplot
photo = jf.loadJson("File/FlickrPhotos.json")

def flickrPlot(coordinate:[]):
    gmap = gmplot.GoogleMapPlotter(lat=float(str(coordinate[0][0]).split(",")[0]),
                                    lng=float(str(coordinate[0][0]).split(",")[1]), zoom=13, apikey=googleKey)
    for x in coordinate:
        gmap.marker(lat=float(str(x[0]).split(',')[0]), lng=float(str(x[0]).split(',')[1]),
                     label=round((x[1] / len(photo) * 100), 1))

    gmap.draw("plot/FlicrkPlot.html")

def gmapPlot(place:[]):
    gmap = gmplot.GoogleMapPlotter(lat=place[0]["lat"], lng=place[0]["long"], zoom=13, apikey=googleKey)

    for x in place:
        gmap.marker(lat=x["lat"], lng=x["long"])
    gmap.draw("plot/GmapPlot.html")

def userPlot(photo:[]):

    for x in photo:
        coordinate = []
        for y in x[1]:
            coordinate.append(y["coordinate"])
        coordinatex = list(dict.fromkeys(coordinate)) #rimuovo i duplicati
        if len(coordinatex) > 1:
            lats = []
            lngs = []
            for z in coordinatex:
                lats.append(float(str(z).split(",")[0]))
                lngs.append(float(str(z).split(",")[1]))
            from Funzioni.Credenziali import googleKey as key
            gmap = gmplot.GoogleMapPlotter(lats[0], lngs[0], 13, apikey=key)
            gmap.scatter(lats, lngs, size=40, marker=True)
            gmap.plot(lats, lngs, 'cornflowerblue')
            gmap.draw("plot/Users/"+str(x[0])+".html")
