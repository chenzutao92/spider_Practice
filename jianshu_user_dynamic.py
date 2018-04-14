import requests
import pymongo
from lxml import etree


client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
timeline = mydb['timeline']

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

def get_time_info(url, page):
    user_id = url.split('/')
    user_id = user_id[4]
    if url.find('page='):
        page = page + 1
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        dd = info.xpath('div/div[1]/div/span/@data-datetime')[0]
        type = info.xpath('div/div[1]/div/span/@data-type')[0]
        timeline.insert_one({'data': dd,'type': type})
    id_infos = selector.xpath('//ul[@class="note-list"]/li/@id')
    if len(id_infos):
        feed_id = id_infos[-1]
        max_id = int(feed_id.split('-')[1]) - 1
        next_url = 'https://www.jianshu.com/users/{0}/timeline?max_id={1}&page={2}'.format(user_id, max_id, page)
        get_time_info(next_url, 1)


if __name__ == '__main__':
    get_time_info('https://www.jianshu.com/users/c098ab8d8e04/timeline', 1)