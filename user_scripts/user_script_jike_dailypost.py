"""
用户脚本：即刻App-一觉醒来世界发生了什么
需要提供关键函数：gen_url_list()和parse_article()
"""
import re
import datetime
import requests
from bs4 import BeautifulSoup


homepage = 'https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68'

def get_url_content(url):
    '''
    获取网页源码，以字符串方式返回
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


def get_html_clip_list():
    '''
    即刻App-一觉醒来世界发生了什么
    https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for li in soup.find('ul', class_='post-list'):
        # print(li.find('div', class_='jsx-3930310120'))
        url_list.append(str(li.find('div', class_='jsx-3930310120')))

    return url_list


def parse_article(html_clip):
    article = {}
    article['url'] = homepage

    date_str_obj = re.search(r'([0-9]+)年([0-9]+)月([0-9]+)日', html_clip)
    date_str = date_str_obj.group()
    y, m, d = int(date_str_obj.group(1)), int(date_str_obj.group(2)), int(date_str_obj.group(3))

    article['title'] = date_str + ' 一觉醒来'
    article['date'] = str(datetime.datetime(y, m, d))
    article['content'] = html_clip

    return article


if __name__ == '__main__':
    html_clip_list = get_html_clip_list()
    
    for html_clip in html_clip_list:
        print(html_clip, '\n')

    article = parse_article(html_clip_list[0])
    print(article)
    print(article.keys())
