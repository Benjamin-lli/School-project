import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import time

## parsing data from existing html
def parse_htmlData(htmlstr):
    sp = BeautifulSoup(htmlstr, 'html.parser')
    ##get house info
    house_list = sp.select('body > div.main-wrap > div.content-wrap > div.content-side-left > ul')

    ##current page list
    page_list = []
    for house in house_list:
        row_list = []

        ## title of the source
        title = house.select('div.list-info > h2 > a')
        title = (title[0].text).strip()
        row_list.append(title)

        ## detail info about house
        infos = house.select('div.list-info > p')

        ## get house type
        house_type = (infos[0].text).strip()
        row_list.append(house_type)

        house_squar = (infos[1].text).strip()
        row_list.append(house_squar)

        house_face = (infos[2].text).strip()
        row_list.append(house_face)

        house_floor = (infos[3].text).strip()
        row_list.append(house_floor)

        page_list.append(row_list)

    return page_list


## 1, data scratching
def request_Data(url):

    req = urllib.request.Request(url)

    ## crate an empty list
    page_data_list = []

    with urllib.request.urlopen(req) as response:
        data = response.read()
        htmlstr = data.decode()
        ## apply the htmlstr with the function and get the data
        L = parse_htmlData(htmlstr)
        ## extend the data to the existing list
        page_data_list.extend(L)

    return page_data_list


## 58.com > beijing > 二手房
url_temp = "http://bj.58.com/ershoufang/pn{}/"

## final data list
data_list = []

for i in range(1, 31):
    ## i for currant pages
    url = url_temp.format(i)
    print(url)
    print("+++++++{}page+++++++".format(i))
    time.sleep(1)
    L = request_Data(url)
    data_list.extend(L)



colname = ['title', 'type', 'squar', 'face', 'floor']

df = pd.DataFrame(data_list, columns=colname)
df.to_csv('/Users/lizhongda/Desktop/data.csv', index = False, encoding='gb18030')