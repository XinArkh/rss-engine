"""
用户脚本：浙大研究生学院通知
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


def gen_url_list(homepage):
    '''
    研究生院网-信息公告-全部公告
    '''
    html = get_url_content(homepage)
    url_list = []
    title_prefix_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('id') == 'wp_news_w2':
            for item in elem.children:
                if item != '\n':
                    title_prefix_list.append('【' + item.find_all('span')[1].a.string + '】')
                    link = item.find_all('a')[-1].get('href')
                    link = 'http://www.grs.zju.edu.cn' + link if link.startswith('/') else link
                    url_list.append(link)
            break

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
    from user_api import url2io_token, url2io_api

    html = get_url_content(url)
    query_string = {'token': url2io_token, 'url': url,}
    headers_url2io = { 'content-type': "text/html", }
    article = requests.post(url2io_api, params=query_string, headers=headers_url2io, data=html.encode('utf-8'))

    if article.status_code != 200:
        article_info = eval(article.text)
        raise Exception('%s: [Response %d] %s' % (article_info['error'], article.status_code, article_info['msg']))

    article_info = article.json().copy()

    pubdate = match_pubdate(html)
    if pubdate:
        article_info['date'] = str(pubdate)

    return article_info


if __name__ == '__main__':
    homepage = 'http://www.grs.zju.edu.cn/'
    url_list, title_prefix_list = gen_url_list(homepage)
    
    for url, prefix in zip(url_list, title_prefix_list):
        print(prefix, url)

    article = parse_article('http://www.grs.zju.edu.cn/2022/0601/c1335a2580931/page.htm')
    print(article)
    print(article.keys())
