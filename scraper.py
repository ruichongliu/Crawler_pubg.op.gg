# Import Necessary Modules
import csv
import time
import json
import requests
from math import floor
from bs4 import BeautifulSoup
from lxml import html

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
serverList = ['na', 'as', 'krjp', 'sea', 'oc', 'eu', 'sa']

def genUrl(userId, season, server, queue_size, mode, after):
    return "https://pubg.op.gg/api/users/%s/matches/recent?season=%s&server=%s&queue_size=%s&mode=%s&after=%s" % (userId, season, server, queue_size, mode, after)

def query(userId, season, server, queue_size, mode, after):

    soup = BeautifulSoup(requests.get(genUrl(userId, season, server, queue_size, mode, after), headers = headers).content, 'html.parser')

    jsonData = json.loads(str(soup))

    try:
        if jsonData['message'] == "":
            return []
    except:
        try:
            matches = jsonData['matches']['items']

        except KeyError:
            return []

        return [] if not matches else list(map(lambda x : [userId, x['participant']['user']['nickname'], x['season'], x['server'], x['queue_size'], x['mode'], x['participant']['stats']['combat']['kda']['kills']], matches))

def main(writer, userIdList, season = '', server = 'na', queue_size = 1, mode = 'tpp', after = 0,):
    t0 = time.time()
    retVal = {}
    counter = 0
    writer.write("Scraper: Scraper Starts\n")
    print("Scraper: Scraper Starts")
    with open('data.csv', 'w', newline = '', encoding = 'UTF-8') as f:
        thewriter = csv.writer(f)
        for i in userIdList:
            writer.write("Scraper: Working on User %s\n" % (i))
            print("Scraper: Working on User %s" % (i))
            for j in serverList:
                for k in range(3):
                    try:
                        for m in query(i, season, j, queue_size, mode, 20 * k):
                            if m == []:
                                continue
                            kills = m[-1]
                            counter += 1
                            if kills not in retVal:
                                retVal[kills] = 1
                            else:
                                retVal[kills] += 1
                            thewriter.writerow(m)
                    except:
                        pass
    t1 = time.time()
    writer.write("Scraper: DONE!! \nTime Used: %s seconds\nData Recorded: %s\n" % (floor(t1 - t0), counter))
    print("Scraper: DONE!! \nTime Used: %s seconds\nData Recorded: %s" % (floor(t1 - t0), counter))
    return retVal
