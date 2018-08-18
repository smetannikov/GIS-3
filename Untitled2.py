
# coding: utf-8

# In[22]:


import requests
import bs4
import csv

import os
dir_path = os.path.dirname(os.path.abspath(r"C:\Users\Lenovo\.PyCharmCE2018.2\config\scratches"))
url = "https://sisfor.osinfor.gob.pe/osinfor/services/capas_osinfor/CONCESION_FORESTAL/MapServer/WmsServer?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&CRS=EPSG:4326&WIDTH=9&HEIGHT=9&LAYERS=0&STYLES=default&FORMAT=image/jpeg&QUERY_LAYERS=0&INFO_FORMAT=text/html&FEATURE_COUNT=100"


bbox =[]

x = 5
y = 5
local_url1 = url+"&X="+str(x)+"&Y="+str(y)

step = 1
startx = - 77.341
starty = - 7.167


bboxx1 = startx
bboxy1 = starty
bboxx2 = startx + step
bboxy2 = starty + step

local_url = local_url1 + "&BBOX=" + str(bboxx1) + "," + str(bboxy1) + "," + str(bboxx2) + "," + str(bboxy2)

for i in range(7):
    for j in range(7):
        local_url = local_url1 + "&BBOX=" + str(bboxx1) + "," + str(bboxy1) + "," + str(bboxx2) + "," + str(bboxy2)
        print(local_url)
#         local_url = "https://sisfor.osinfor.gob.pe/osinfor/services/capas_osinfor/CONCESION_FORESTAL/MapServer/WmsServer?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&BBOX=-13.4777410000000000,-80.9995590000000050,4.0101770000000000,%20-74.8589340000000021&CRS=EPSG:4326&WIDTH=100&HEIGHT=100&LAYERS=0&STYLES=default&FORMAT=image/jpeg&QUERY_LAYERS=0&INFO_FORMAT=text/html&FEATURE_COUNT=100&X=50&Y=60"
        bboxy1 += step
        bboxy2 += step 
        r = requests.get(local_url)
        # print(r.text)
        soup = bs4.BeautifulSoup(r.text, "lxml")
        try:
            table = soup.find('table').findAll('tr')
        
            headers_html = table[0].findAll('th')
            content = []
            if len(table) > 1:
                for line in range(1,len(table)):
                    ct = table[line].findAll('td')
                    content.append([cont.contents[0] for cont in ct])
                    # add x and y
                    cx =((bboxx2 + bboxx1) / 2)
                    cy = ((bboxy2 + bboxy1) /  2)          
                    content[-1].append(cx)              
                    content[-1].append(cy)


            headers = [head.contents[0] for head in headers_html]
            headers.append("x")
            headers.append("y")

            print(len(headers), headers)
            print(len(content), content)
            data_file = os.path.join(dir_path, 'data.csv')
            with open(data_file, 'w', encoding="utf-8") as outcsv:
                # writer = csv.writer(outcsv)
                # writer.writerow(headers)
                writer = csv.DictWriter(outcsv, delimiter=',', lineterminator='\n', fieldnames=headers)
                if not os._exists(data_file):
                    writer.writeheader()  # file doesn't exist yet, write a header

                dict_to_write = {}
                for c in content:
                    for h in range(len(headers)):
                        dict_to_write[headers[h]] = c[h]
                    print(dict_to_write)
                    writer.writerow(dict_to_write)
                    dict_to_write={}
        except Exception:
            print("Empty page")
            pass

    bboxx1 += step
    bboxx2 += step
    bboxy1 = starty
    bboxy2 = starty + step

