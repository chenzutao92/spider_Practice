import requests
import time
from bs4 import BeautifulSoup


# 使用request， bs4抓取小猪短租网信息
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


def judgment_set(class_name):
    if class_name == ['member_girl_ico']:
        return '女'
    else:
        return '男'


def get_page(url):
    # url = 'http://gz.xiaozhu.com/search-duanzufang-p{0}-0/' + format(offset)
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#page_list > ul > li > a')
    for link in links:
        href = link.get("href")
        get_info(href)


def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tittles = soup.select('div.pho_info > h4')
    addresses = soup.select('span.pr5')
    prices = soup.select('#pricePart > div.day_l > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span')
    for tittle, addresse, price, img, name, sex in zip(tittles, addresses, prices, imgs, names, sexs):
        data = {
            'tittle': tittle.get_text().strip(),
            'addresse': addresse.get_text().strip(),
            'price': price.get_text(),
            'img': img.get("src"),
            'name': name.get_text(),
            'sex': judgment_set(sex.get("class"))
        }
        print(data)


if __name__ == '__main__':
    urls = ['http://gz.xiaozhu.com/search-duanzufang-p{0}-0/'.format(number) for number in range(1, 11)]
    for single_url in urls:
        get_page(single_url)
        time.sleep(2)