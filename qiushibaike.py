import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

info_lists = []


def judgment_sex(class_name):
    if class_name == "womenIcon":
        return "女"
    else:
        return "男"


def get_info(url):
    res = requests.get(url, headers=headers)
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    levels = re.findall('<div class="articleGender manIcon">(.*?)</div>', res.text, re.S)
    sexs = re.findall('<div class="articleGender (.*?)">', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i> 好笑</span>', res.text, re.S)
    comments = re.findall('<i class="number">(\d+)</i> 评论', res.text, re.S)
    for id, level, sex, content, laugh, comment in zip(ids, levels, sexs, contents, laughs, comments):
        info = {
            'id': id,
            'level': level,
            'sex': judgment_sex(sex),
            'content': content,
            'laugh': laugh,
            'comment': comment
        }
        info_lists.append(info)


if __name__ == '__main__':
    urls = ["https://www.qiushibaike.com/text/page/{}/".format(str(i)) for i in range(1, 14)]
    for url in urls:
        get_info(url)

    for info_list in info_lists:
        f = open('qiushi.txt', 'a+')
        try:
            f.write(info_list['id']+'\n')
            f.write(info_list['level']+'\n')
            f.write(info_list['sex']+'\n')
            f.write(info_list['content']+'\n')
            f.write(info_list['laugh']+'\n')
            f.write(info_list['comment']+'\n\n')
            f.close()
        except UnicodeEncodeError:
            pass
