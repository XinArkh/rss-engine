"""
用户脚本：浙大研究生学院通知
需要提供关键函数：gen_url_list()和parse_article()

"""
import re
import datetime
import requests
from bs4 import BeautifulSoup
import os, sys
sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
import url2article


def get_url_content(url):
    '''
    获取网页源码，以字符串方式返回
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


def gen_url_list(homepage):
    '''
    研究生院网-信息公告-全部公告
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    elem = soup.find('div', id='wp_news_w09')
    for item in elem.children:
        if item != '\n':
            link = item.a['href']
            link = 'http://www.grs.zju.edu.cn' + link if link.startswith('/') else link
            url_list.append(link)

    return url_list


def match_pubdate(html):
    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find('div', class_='article-title').p.span.text
    pubdate = datetime.datetime.strptime(date, '%Y-%m-%d')
    return pubdate


def parse_article(url):
    """解析文章信息"""

    article_info = url2article.parse_article(url)

    # 抓取特定位置的日期信息，提高日期精度
    html = get_url_content(url)
    pubdate = match_pubdate(html)
    if pubdate:
        article_info['date'] = str(pubdate)

    return article_info


if __name__ == '__main__':
    homepage = 'http://www.grs.zju.edu.cn/qbgg/list.htm'
    url_list = gen_url_list(homepage)
    
    for url in url_list:
        print(url)

    article = parse_article(url_list[0])
    print(article)
    print(article.keys())
