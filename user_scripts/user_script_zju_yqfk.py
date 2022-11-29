"""
用户脚本：浙大疫情防控工作网页通知
需要提供关键函数：
    get_url_list() - 用于生成所有关注栏目的通知链接（及对应前缀）
    parse_article() - 用于解析通知文章信息

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


def get_url_list_subpage(homepage):
    '''
    获取分页栏目的网址列表，由于每个栏目结构相同，因此可使用同一个函数获取
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    elem = soup.find('div', id='wp_news_w6')
    for item in elem.ul.children:
        if item != '\n':
            link = item.a['href']
            link = 'https://yqfk.zju.edu.cn' + link if link.startswith('/') else link
            url_list.append(link)
    return url_list


def get_url_list():
    '''
    生成所有关注栏目的通知链接及对应前缀
    '''
    hp1 = 'https://yqfk.zju.edu.cn/66536/list.htm' # 疫情防控工作-通知公告
    hp2 = 'https://yqfk.zju.edu.cn/66628/list.htm' # 疫情防控工作-上级文件
    hp3 = 'https://yqfk.zju.edu.cn/66629/list.htm' # 疫情防控工作-防控形势

    url_list1 = get_url_list_subpage(hp1)
    url_list2 = get_url_list_subpage(hp2)
    url_list3 = get_url_list_subpage(hp3)

    url_list = url_list1 + url_list2 + url_list3
    title_prefix_list = ['【通知公告】'] * len(url_list1) + ['【上级文件】'] * len(url_list2) + ['【防控形势】'] * len(url_list3)

    return url_list, title_prefix_list


def match_pubdate(html):
    '''
    手动抓取通知页面的日期信息，提高日期精度
    '''
    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find('span', class_='arti_update').text[5:]
    pubdate = datetime.datetime.strptime(date, '%Y-%m-%d')
    return pubdate


def parse_article(url):
    '''
    解析文章信息
    '''
    article_info = url2article.parse_article(url)
    html = get_url_content(url)
    pubdate = match_pubdate(html)
    if pubdate:
        article_info['date'] = str(pubdate)

    return article_info


if __name__ == '__main__':
    url_list, title_prefix_list = get_url_list()
    
    for url, title_prefix in zip(url_list, title_prefix_list):
        print(title_prefix, url)

    article = parse_article(url_list[0])
    print(article)
    print(article.keys())
