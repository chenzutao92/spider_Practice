from lxml import etree
import requests
import pymongo
import re
import json
from multiprocessing import Pool
from requests import HTTPError

clinet = pymongo.MongoClient('localhost', 27017)
mydb = clinet['mydb']
sevenday = mydb['sevenday']

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


def get_url(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        article_url_part = info.xpath('div/a/@href')[0]
        get_info(article_url_part)


def get_info(url):
    article_url = 'https://www.jianshu.com' + url
    html = requests.get(article_url, headers=headers)
    selector = etree.HTML(html.text)
    author = selector.xpath('//span[@class="name"]/a/text()')[0]
    article = selector.xpath('//h1[@class="title"]/text()')[0]
    date = selector.xpath('//span[@class="publish-time"]/text()')[0]
    view = re.findall('"views_count":(.*?),', html.text, re.S)[0]
    word = re.findall('"public_wordage":(.*?),', html.text, re.S)[0]
    commetn = re.findall('"comments_count":(.*?),', html.text, re.S)[0]
    like = re.findall('"likes_count":(.*?),', html.text, re.S)[0]
    id = re.findall('"id":(.*?),', html.text, re.S)[0]

    gain_url = 'https://www.jianshu.com/notes/{}/rewards?count=20'.format(id)
    wb_data = requests.get(gain_url, headers=headers)
    json_data = json.loads(wb_data.text)
    gain = json_data['rewards_count']

    include_list = []
    include_urls = ['https://www.jianshu.com/notes/{0}/included_collections?page={1}'.format(id, str(i)) for i in range(1,10)]
    for include_url in include_urls:
        try:
            html = requests.get(include_url, headers=headers)
            json_data = json.loads(html.text)
            includes = json_data['collections']
            if len(includes) == 0:
                pass
            else:
                for include in includes:
                    include_title = include['title']
                    include_list.append(include_title)
        except HTTPError:
            pass

        info = {
        'author': author,
        'article': article,
        'date': date,
        'word': word,
        'view': view,
        'like': like,
        'gain': gain,
        'include_list': include_list,
    }
    sevenday.insert_one(info)


if __name__ == '__main__':
    urls = ['https://www.jianshu.com/trending/weekly?pange={}'.format(str(i)) for i in range(1, 10)]
    pool = Pool(processes=4)
    pool.map(get_url, urls)