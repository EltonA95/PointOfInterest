bbox = "12.343140,41.796729,12.625122,42.000419"
import Funzioni.JsonFunction as jf
import Processing.FlickrProcessing as fp
import Processing.Statistica as stat
import Processing.Plot as plt


photo = fp.photoProcessing(bbox=bbox,start_year=2019, start_month=6,start_day=1,
                           max_year=2019, max_month=6, max_day=30)
                           
coordinate = stat.mostVisisted(photo,20)
gmapPlace = coordinate[0]
flicrkPlace = coordinate[1]

plt.gmapPlot(gmapPlace)
plt.flickrPlot(flicrkPlace)

"""

photos = fp.photoProcessing(bbox=bbox,start_year=2019, start_month=6,start_day=1,
                           max_year=2019, max_month=6, max_day=7)
plt.userPlot(photos)

"""
