# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv, time

from getrandomheader import getrandomheader
from ippool import get_random_ip
#1. 下载解析网页
def scrapeasoniaogebiji(appleid):
    #1.1 构造url
    url = 'http://aso.niaogebiji.com/app/samepubapp?id={}'.format(appleid)
    #1.2 下载网页
    response = requests.get(url, headers = getrandomheader(), proxies = get_random_ip())
    html = response.text
    #1.3 解析网页
    soup = BeautifulSoup(html, 'html.parser')
    artistname = soup.find('div',{'class': 'artistnamezh'}).get_text() #获取开发者名称
    ranktable = soup.find('tbody', {'id': 'contentRank'})
    publisher_num = len(ranktable.find_all('tr', {'class': 'competi-list'})) #同开发者应用数

    data = [appleid, artistname, publisher_num]

    return data

#2. 存储数据
def savedata(data):
    with open('data/output/publisher_num.csv','a+',newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(data)

#3. 主程序
def main(appleidlist, usedidlist):
    for appleid in appleidlist:
        if appleid in usedidlist:
            continue
        try:
            savedata(scrapeasoniaogebiji(appleid))
        except:
            print('error {}'.format(appleid))
            time.sleep(5)
            continue
        with open('data/output/usedid.txt','a+') as f:
            f.write('\n{}\n'.format(appleid))
        print('success {}'.format(appleid))
        time.sleep(5)

if __name__ == '__main__':
    with open('data/input/appleid.txt', 'r') as f:
        appleidlist = [id.replace('\n','') for id in f.readlines()]
    with open('data/output/usedid.txt','r') as f2:
        usedidlist  = [id.replace('\n','') for id in f2.readlines()]

    main(appleidlist,usedidlist)