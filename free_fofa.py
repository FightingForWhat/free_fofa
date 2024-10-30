# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Time    : 2021-03-20
# @Author  :  
# @FileName: free_fofa.py
# version: 1.0.0

import requests
from lxml import etree
import base64
import re
import time
import base_auto
import config_auto
import datetime
import os
from urllib.parse import quote

def fofa_spider_auto():
    search_key = input('[*] 请输入fofa搜索关键字: ')
    # print('search_key =' + search_key)
    # print(searchbs64)

    limit_l = int(input('[*] 请输入需要导出多少天的数据：'))

    for limit_d in range(1, limit_l+1):

        i = limit_d - 2
        time_before = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        time_after = (datetime.datetime.now() - datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d")

        if 'before' in search_key:
            search_key = search_key.split('&& before')[0]
            search_key = search_key.strip(' ')
            search_key = search_key + ' && ' + 'before="' + str(time_before) + '"' + ' && ' + 'after="' + str(time_after) + '"'
        else:
            search_key = search_key + ' && ' + 'before="' + str(time_before) + '"' + ' && ' + 'after="' + str(
                time_after) + '"'

        print('[*] 搜索词： ' + search_key)

        searchbs64 = quote(str(base64.b64encode(search_key.encode()), encoding='utf-8'))

        # searchbs64 = (str(base64.b64encode(config.SearchKEY.encode('utf-8')), 'utf-8'))
        print("[*] 爬取页面为:https://fofa.so/result?&qbase64=" + searchbs64)
        html = requests.get(url="https://fofa.so/result?&qbase64=" + searchbs64, headers=config_auto.header).text
        pagenum = re.findall('>(\d*)</a> <a class="next_page" rel="next"', html)

        StartPage = 1
        if pagenum:
            StopPage = int(pagenum[0])
            print("[*] 该关键字存在页码: " + str(pagenum[0]))
            if StopPage <= 5:
                pass
            else:
                StopPage = 5
        else:
            StopPage = 1
            print("[*] 该关键字存在页码: " + '1')


        doc = open('./tmp/' + str(limit_d) + '.txt', "a+")
        for i in range(StartPage, StopPage + 1):
            print('\n' + "[*] ----------------正在爬取第" + str(i) + "页----------------" + '\n')
            pageurl = requests.get('https://fofa.so/result?page=' + str(i) + '&qbase64=' + searchbs64,
                                   headers=config_auto.header)
            tree = etree.HTML(pageurl.text)
            urllist = tree.xpath('//div[@class="fl box-sizing"]/div[@class="re-domain"]/a[@target="_blank"]/@href')
            urllist = [value.strip('\n').strip(' ').strip('\n') for value in urllist if
                       len(value.strip('\n').strip(' ').strip('\n')) != 0]
            for j in urllist:
                print('[+]' + j)
                doc.write(j + "\n")
            time.sleep(config_auto.TimeSleep)
        doc.close()

        print('\n' + '\n' + '[*] ------' + str(time_after) + '数据爬取完毕------当前进度: [' + str(limit_d) + '/' + str(limit_l) + ']' + '------\n' + '\n')
    print('[*] 数据爬取完毕...\n')
    return


def disposal_data():
    print('[*] 开始同步数据...\n')
    # dirnum = len([lists for lists in os.listdir('./tmp/') if os.path.isdir(os.path.join('./tmp/', lists))])
    dirnum = len([lists for lists in os.listdir('./tmp/') if os.path.isfile(os.path.join('./tmp/', lists))])

    i = 0
    for list_num in range(1, dirnum + 1):

        print('[*] 将文件 ' + str(list_num) + '.txt 中的数据同步至 result_auto.txt\n')
        f = open('./tmp/' + str(list_num) + '.txt', "r", encoding="gb18030")
        f_read = f.readlines()
        r = open('./result_auto.txt', "r", encoding="gb18030")
        r_read = r.read()
        result_auto = open('./result_auto.txt', 'a+')
        for url_spider in f_read:
            if url_spider in r_read:
                url_spider = url_spider.strip('\n')
                print('[-] ' + url_spider + '...has been backuped')
            else:
                url_spider = url_spider.strip('\n')
                print('[+] 同步 ' + url_spider)
                result_auto.write(url_spider + '\n')
                i += 1
        print()
        result_auto.close()
    print('\n[*] 同步结束-----共计同步数据：' + str(i) + '\n')


def delete_tmp():
    print('[*] 删除缓存中...\n')
    dirnum = len([lists for lists in os.listdir('./tmp/') if os.path.isfile(os.path.join('./tmp/', lists))])
    for delete_num in range(1, dirnum + 1 ):

        os.remove('./tmp/' + str(delete_num) + '.txt')
        print('[-] 删除文件 ' + str(delete_num) + '.txt')
    print('\n[*] 删除完毕\n\n')

def main():
    base_auto.logo()
    base_auto.checkSession()
    base_auto.init()

    fofa_spider_auto()
    disposal_data()
    delete_tmp()

if __name__ == '__main__':
    main()

