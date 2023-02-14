"""
用户脚本：浙大机械学院通知
需要提供关键函数：gen_url_list()和parse_article()

"""
import re
import datetime
import requests
from bs4 import BeautifulSoup


def get_url_content(url):
    '''
    获取网页源码，以字符串方式返回
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


def get_url_list_tzgg(homepage):
    '''
    《通知公告》板块
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('frag') == '窗口8':
            url_items = elem.ul
            for item in url_items.children:
                if item != '\n':
                    link = item.a.get('href')
                    link = 'http://me.zju.edu.cn' + link if link.startswith('/meoffice/') else link
                    url_list.append(link)
            break
    return url_list


def get_url_list_yjsjy(homepage):
    '''
    《研究生教育》板块
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('frag') == '窗口9':
            url_items = elem.ul
            for item in url_items.children:
                if item != '\n':
                    link = item.get('href')
                    link = 'http://me.zju.edu.cn' + link if link.startswith('/meoffice/') else link
                    url_list.append(link)
            break
    return url_list


def get_url_list_xsgz(homepage):
    '''
    《学生工作》板块
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('frag') == '窗口9':
            url_items = elem.ul
            for item in url_items.children:
                if item != '\n':
                    link = item.get('href')
                    link = 'http://me.zju.edu.cn' + link if link.startswith('/meoffice/') else link
                    url_list.append(link)
            break
    return url_list


def gen_url_list(homepage):
    hp1, hp2, hp3 = homepage

    url_list1 = get_url_list_tzgg(hp1)
    url_list2 = get_url_list_yjsjy(hp2)
    url_list3 = get_url_list_xsgz(hp3)

    url_list = url_list1 + url_list2 + url_list3
    title_prefix_list = ['【通知公告】'] * len(url_list1) + ['【研究生教育】'] * len(url_list2) + ['【学生工作】'] * len(url_list3)

    return url_list, title_prefix_list


def match_pubdate(html):
    '''
    尝试在html文本中匹配【时间：yyyy-mm-dd】格式的字符片段，若匹配到则将其作为发布时间返回
    p.s. api自带的时间提取功能错误率比较高，经常把正文中的时间提取为发表时间
    '''
    searchObj = re.search(r'时间：[0-9]{4}-[0-9]{2}-[0-9]{2}|&#x65F6;&#x95F4;&#xFF1A;[0-9]{4}-[0-9]{2}-[0-9]{2}', html)
    # 【&#x65F6;&#x95F4;&#xFF1A;】是【时间：】的unicode字符，不知道为什么有时会以此形式出现

    if searchObj:
        pubdate = datetime.datetime.strptime(searchObj.group(0)[-10:], '%Y-%m-%d')
        return pubdate
    else:
        return None


def parse_article(url):
    """解析文章信息"""
    
    import os, sys
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
    import url2article

    article_info = url2article.parse_article(url)

    html = get_url_content(url)
    pubdate = match_pubdate(html)
    if pubdate:
        article_info['date'] = str(pubdate)

    return article_info


if __name__ == '__main__':
    homepage1 = 'http://me.zju.edu.cn/meoffice/'
    homepage2 = 'http://me.zju.edu.cn/meoffice/6440/list.htm'
    homepage3 = 'http://me.zju.edu.cn/meoffice/6469/list.htm'

    homepage = [homepage1, homepage2, homepage3]
    url_list, title_prefix_list = gen_url_list(homepage)

    for url, title_prefix in zip(url_list, title_prefix_list):
        print(title_prefix, url)

    article = parse_article(url_list[0])
    print(article)
    print(article.keys())
