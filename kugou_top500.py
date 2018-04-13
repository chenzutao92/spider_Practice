import requests
import time
from bs4 import BeautifulSoup


# 使用request， bs4抓取酷狗top500
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select("span.pc_temp_num")
    titles = soup.select("#rankWrap > div.pc_temp_songlist > ul > li")
    times = soup.select("span.pc_temp_tips_r > span")
    for rank, title, time in zip(ranks, titles, times):
        data = {
            'rank': rank.get_text().strip(),
            'singer': title.get("title").split("-")[0],
            'song': title.get("title").split("-")[1],
            'time': time.get_text().strip()
        }
        print(data)


if __name__ == '__main__':
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)]
    for url in urls:
        get_info(url)
        time.sleep(5)