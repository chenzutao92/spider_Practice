import requests
import json
import lxml
import pymongo
import time


client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
lagou = mydb['lagou']

headers = {
    'Cookie': 'index_location_city=%E5%B9%BF%E5%B7%9E; _ga=GA1.2.1318090156.1519178979; user_trace_token=20180221100940-46188daf-16ac-11e8-8cab-525400f775ce; LGUID=20180221100940-46189115-16ac-11e8-8cab-525400f775ce; WEBTJ-ID=20180414230336-162c4aed9aae4-094724e746beed-3a614f0b-1327104-162c4aed9ab1ea; _gid=GA1.2.2140009230.1523718216; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521409084,1521409092,1522720226,1523718217; LGSID=20180414230336-020b4b7e-3ff5-11e8-b866-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3D%25E6%258B%2589%25E5%258B%25BE; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; X_HTTP_TOKEN=8b44293725345a17c893ba0c41a1e691; LG_LOGIN_USER_ID=4dbb3da1f07bbc962be07db1058da2adce967832748d5801; _putrc=10CA35F8B5BE121D; JSESSIONID=ABAAABAAAIAACBI4B4BD4FF42DD508E48D5FA8CB5215E33; login=true; unick=%E9%99%88%E7%A5%96%E6%BB%94; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=46; gate_login_token=e41f1a58efc5c2318a4c1895b03d31ceab38bb39b12acd17; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523718255; LGRID=20180414230415-18cdcceb-3ff5-11e8-b868-5254005c3644; SEARCH_ID=b92d1b8cd0d04445a9bc3fd5bcba6a55',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Connection': 'keep-alive'
}


def get_page(url, params):
    html = requests.post(url, data=params, headers=headers)
    json_data = json.loads(html.text)
    total_Count = json_data['content']['positionResult']['totalCount']
    page_number = int(total_Count/15) if int(total_Count/15) < 30 else 30
    get_info(url, page_number)


def get_info(url, page):
    for pn in range(1, page+1):
        params = {
            'first': 'true',
            'pn': 'str(pn)',
            'kd': 'python'
        }
        try:
            html = requests.post(url, data=params, headers=headers)
            json_data = json.loads(html.text)
            results = json_data['content']['positionResult']['result']
            for result in results:
                infos = {
                    'businessZones': result['businessZones'],
                    'city': result['city'],
                    'companyFullName': result['companyFullName'],
                    'companyLabelList': result['companyLabelList'],
                    'district': result['district'],
                    'education': result['education'],
                    'explain': result['explain'],
                    'firstType': result['firstType'],
                    'formatCreateTime': result['formatCreateTime'],
                    'gradeDescription': result['gradeDescription'],
                    'imState': result['imState'],
                    'industryField': result['industryField'],
                    'jobNature': result['jobNature'],
                    'positionAdvantage': result['positionAdvantage'],
                    'salary': result['salary'],
                    'secondType': result['secondType'],
                    'workYear': result['workYear'],
                }
                lagou.insert_one(infos)
                time.sleep(2)
        except requests.exceptions.ConnectionError:
            pass


if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    params = {
        'first': 'true',
        'pn': 'str(pn)',
        'kd': 'python'
    }
    get_page(url, params)