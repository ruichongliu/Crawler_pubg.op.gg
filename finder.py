import time
import requests
from math import floor
from lxml import html
from functools import reduce
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

def main(writer, user0):
    t0 = time.time()
    def nameToId(userList):
        def f(user):
            print("Finder: Translating User %s..." % (user))
            writer.write("Finder: Translating User %s...\n" % (user))
            soup = BeautifulSoup(requests.get("https://pubg.op.gg/user/%s?server=as" % (user), headers = headers).content, 'html.parser')
            try:
                retVal = soup.body.div.section.find('div', 'content__wrapper--player-summary').find('div', 'content__inner').find('div', 'player-summary').div.div.attrs['data-user_id']
            except:
                retVal = "59fd962cab1fff00019e0759"
            return retVal
        return list(map(f, userList))

    def userMap(userList):
        def g(user):
            print("Finder: Collecting Friends of User %s..." % (user))
            writer.write("Finder: Collecting Friends of User %s...\n" % (user))

            driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
            driver.get("https://pubg.op.gg/user/%s?server=as" % (user))

            xpath = ["/html/body/div[@class='pubg pubg--player']/section[@class='container']/div[@class='content__wrapper']/div[@class='content__inner']/div[@class='overview']/div[@class='overview__row']/div[@class='overview__column overview__column--right']/div[2]/div/ul[@class='total-played-game__list']/li[@class='total-played-game__item'][1]/div[@class='played-game ']/div[@class='played-game__summary']/div[@class='played-game__column played-game__column--btn']/button[@class='sp__toggle played-game__btn played-game__btn--detail']",\
             "/html/body/div[@class='pubg pubg--player']/section[@class='container']/div[@class='content__wrapper']/div[@class='content__inner']/div[@class='overview']/div[@class='overview__row']/div[@class='overview__column overview__column--right']/div[2]/div/ul[@class='total-played-game__list']/li[@class='total-played-game__item'][1]/div[@class='played-game played-game--top10']/div[@class='played-game__summary']/div[@class='played-game__column played-game__column--btn']/button[@class='sp__toggle played-game__btn played-game__btn--detail']",\
             "/html/body/div[@class='pubg pubg--player']/section[@class='container']/div[@class='content__wrapper']/div[@class='content__inner']/div[@class='overview']/div[@class='overview__row']/div[@class='overview__column overview__column--right']/div[2]/div/ul[@class='total-played-game__list']/li[@class='total-played-game__item'][1]/div[@class='played-game played-game--win']/div[@class='played-game__summary']/div[@class='played-game__column played-game__column--btn']/button[@class='sp__toggle played-game__btn played-game__btn--detail']"]

            flag = 0
            while True:
                try:
                    elem = driver.find_element_by_xpath(xpath[flag])
                    break
                except IndexError:
                    raise IndexError
                except:
                    flag += 1
            actions = ActionChains(driver)
            actions.click(elem).perform()

            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            return soup.body.div.section.find_all('div', 'content__wrapper')[1].find('div', 'content__inner').div.div.find('div', 'overview__column--right').find_all('div')[1].find('ul', 'total-played-game__list').li.div.find('div', 'played-game__detail').div.find_all('div', 'played-game-statistics__contents')[1].div.find('div', 'played-game-statistics__content').div.table.tbody.find_all('tr')

        x = lambda x: x.find_all('td')[1].div.find_all('a')
        y = lambda y: y.string
        z = lambda x, y: x + y
        return list(set(list(map(y, reduce(z, list(map(x, reduce(z, list(map(g, userList))))))))))

    q = [user0]
    writer.write("Finder: Starting with User %s...\n" % (user0))
    print("Finder: Starting with User %s..." % (user0))
    q = nameToId(userMap(q))
    with open('userIdList.txt', 'w', newline = '', encoding = 'UTF-8') as f:
        for i in q:
            f.write("%s\n" % (i))
    t1 = time.time()
    writer.write("Finder: DONE!! \nTime Used: %s seconds\nUsers Captured: %s\n" % (floor(t1- t0), len(q)))
    print("Finder: DONE!! \nTime Used: %s seconds\nUsers Captured: %s" % (floor(t1- t0), len(q)))
