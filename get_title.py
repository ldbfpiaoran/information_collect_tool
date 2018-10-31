# pylint: disable=no-member
import requests
import json
import aiohttp
import asyncio
import time
import sys
from functools import reduce 
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
semaphore = asyncio.Semaphore(200)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}


def ip_into_int(ip):
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_Intranet(ip):    # 判断内网ip
    if str(ip).startswith("127.0.0"):
	    return True
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c


async def fetch(session, url):
    async with session.get(url,ssl=False,headers=headers) as response:
        res = await response.text()
        soup = BeautifulSoup(res, 'lxml')
        return soup.title.get_text()
        
        



async def scan(url):
    port = [80,443,8443,8000,8080,8081,81]
    async with semaphore:
        for p in port:
            try:
                if p == 443 or p == 8443:
                    u = 'https://'+url+':'+str(p)
                else:
                    u = 'http://'+url+':'+str(p)
                async with aiohttp.ClientSession() as session:
                    res = await fetch(session, u)
                    print(u+'\t'+res)
                    result.append(u+'\t'+str(res)+'\n')
            except Exception as e:
                pass


file_name = sys.argv[1]
# file_name = 'baidu_name.txt'
scan_list = []

with open(file_name ,'r') as f:
    for line in f:
        line = line.split('\t')
        domain = line[0]
        ip = line[1].replace('\n','').replace('[','').replace(']','').replace("'",'').split(',')[0]
        if is_Intranet(ip) is False:
            scan_list.append(domain)


result = []
with open('result.txt','a',errors="ignore") as e:
    # scan_list = ['xss.cuijianxiong.top','mgate.baidu.com','trends.baidu.com']
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(scan(url)) for url in scan_list]
    loop.run_until_complete(asyncio.wait(tasks)) 
    print('over')
    for li in result:
        e.write(li)
