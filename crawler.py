from bs4 import BeautifulSoup
from urllib import request
import config


def generateUrl(searchName):
    url=config.url
    searchUrl=config.searchUrl
    if searchName !="":
        urlName = request.quote(searchName)
        url=searchUrl+urlName
    result = crawler(url)
    return result


def crawler(url):
    response = request.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content,'lxml')
    tables=soup.findAll('table')
    result = []
    if len(tables) > 1:
        table = tables[1]
        bangumiList=[]
        magnetList=[]
        for id,tr in enumerate(table.findAll('tr')):
            if id!=0:
                tds = tr.findAll('td')
                bangumis = tds[2]
                bangumi = bangumis.findAll('a')
                if len(bangumi)>1:
                    bangumiList.append(bangumi[1].get_text().replace('\n', '').replace('\t', ''))
                else:
                    bangumiList.append(bangumi[0].get_text().replace('\n', '').replace('\t', ''))
                magnet=tds[3].findAll('a')
                magnetList.append(magnet[0]['href'])
        result.append(bangumiList)
        result.append(magnetList)
    return result
