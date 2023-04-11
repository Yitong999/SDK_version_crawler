import json

import requests
import random
from time import  sleep
from  lxml import etree
from lxml.html import fromstring
url = None
append = "?page="
pageNum = 0
def get_agent():
    return random.choice(
        [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Mozilla/5.0 (Windows NT 10.0; Win 64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        ]
    )
def parse_html(root):
    sec_list =root.xpath('//section')
    r = list()
    for sec in sec_list:
        title = sec.xpath(".//h2[@class='sr-only']/text()")[0]
        time = sec.xpath(".//relative-time/text()")[0]
        fds = sec.xpath('.//ul')
        fts = sec.xpath('.//h3/text()')
        f = list()
        for i in range(0,len(fds)):
            li = list()
            try:
                ft = fts[i]
            except Exception as e:
                ft = ''
            fd = fds[i]
            fdd = fd.xpath('.//li')
            for d in fdd:
                li.append(fromstring(etree.tostring(d,encoding='utf-8').decode('utf-8')).text_content())
            f.append({'title':ft,'description':li})
        with open('./output.json',mode='a',encoding='utf-8') as f1:
            f1.write(json.dumps({'version':title,'features':f,'date':time}))
            f1.write('\n')
def first_init():
    global pageNum
    headers = {

    }
    pageIndex = 1
    headers['User-Agent'] = get_agent()
    resp = None
    while True:
        try:
            resp = requests.get(url,headers=headers,timeout=5)
            break
        except Exception as e:
            print('Internet Err, Retrying ...')
            sleep(1)
            continue
    if resp is not None:
        resp.encoding = 'utf-8'
        text = resp.text
        root = etree.HTML(text)
        alist = root.xpath('//div[@role="navigation"]/a')
        if len(alist) == 0:
            return
        last_a = alist[-3]
        pageNum = int(last_a.xpath('./text()')[0])
        parse_html(root)
    else:
        return
def getpage(page):
    headers = {

    }
    pageIndex = 1
    headers['User-Agent'] = get_agent()
    resp = None
    while True:
        try:
            resp = requests.get(f'{url}{append}{page}', headers=headers, timeout=5)
            break
        except Exception as e:
            print('Internet Err, Retrying ...')
            sleep(1)
            continue
    if resp is not None:
        resp.encoding = 'utf-8'
        text = resp.text
        root = etree.HTML(text)
        parse_html(root)
def run():
    headers = {

    }
    pageIndex = 1
    headers['User-Agent'] = get_agent()
    first_init()
    print('Successfully get [1] page')
    sleep(1)
    for i in range(2,pageNum+1):
        getpage(i)
        print(f'Successfully get [{i}] page')
        sleep(1)
if __name__ == '__main__':
    url  = input('input url here\n')
    run()