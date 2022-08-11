import re
import datetime
import requests
from bs4 import BeautifulSoup


def get_bs(url):
    '''
    获取网页源码，以字符串方式返回
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'xml')
    
    return soup


def gen_url_list(homepage):
    url_list = []
    soup = get_bs(homepage)
    for elem in soup.find_all('item'):
        url_list.append(elem.link.text)

    return url_list


def parse_article(url, homepage):
    import os, sys
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
    import url2article

    article_info = url2article.parse_article(url)
    
    soup = get_bs(homepage)
    for elem in soup.find_all('item'):
        if elem.link.text == article_info['url']:
            article_info['date'] = str(datetime.datetime.strptime(elem.pubDate.text, '%a, %d %b %Y %H:%M:%S +0800'))
            article_info['author'] = elem.author.text
            break

    return article_info


if __name__ == '__main__':
    homepage = 'https://sspai.com/feed'
    url_list = gen_url_list(homepage)
    print(url_list)
    article = parse_article(url_list[0], homepage)
    print(article)
