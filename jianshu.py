import requests
from lxml import etree
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
jianshu_shouye = mydb['jianshu_shouye']

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


def get_jsanshu_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')

    for info in infos:
        try:
            author = info.xpath('div/div[1]/div/a/text()')[0]
            time = info.xpath('div/div[1]/div/span/@data-shared-at')[0]
            title = info.xpath('div/a/text()')[0]
            content = info.xpath('div/p/text()')[0].strip()
            view = info.xpath('div/div[2]/a[1]/text()')[1].strip()
            comment = info.xpath('div/div[2]/a[2]/text()')[1].strip()
            like = info.xpath('div/div[2]/span[1]/text()')[0].strip()
            rewards = info.xpath('div/div[2]/span[2]/text()')
            if len(rewards) == 0:
                reward = "无"
            else:
                reward = rewards[0].strip()

            data = {
                'author': author,
                'time': time,
                'title': title,
                'content': content,
                'view': view,
                'comment': comment,
                'like': like,
                'reward': reward,
            }
            jianshu_shouye.insert_one(data)
        except IndexError:
            pass


if __name__ == '__main__':
    urls = ['https://www.jianshu.com/c/bDHhpK?order_by=commented_at&page={}'.format(str(i)) for i in range(1, 100)]
    p = Pool(processes=4)
    p.map(get_jsanshu_info, urls)