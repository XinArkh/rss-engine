import re
import datetime
import requests

from user_api import url2io_token, url2io_api


def get_url_content(url):
    '''
    获取网页源码，以字符串方式返回
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


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


def get_article(url):
    html = get_url_content(url)
    query_string = {'token': url2io_token, 'url': url,}
    headers = { 'content-type': "text/html", }
    article = requests.post(url2io_api, params=query_string, headers=headers, data=html.encode('utf-8'))

    if article.status_code != 200:
        article_info = eval(article.text)
        raise Exception('%s: [Response %d] %s' % (article_info['error'], article.status_code, article_info['msg']))

    article_info = article.json().copy()

    pubdate = match_pubdate(html)
    if pubdate:
        article_info['date'] = str(pubdate)

    return article_info


if __name__ == '__main__':
    # example
    article = get_article('http://ygb.zju.edu.cn/2022/0304/c31564a2503309/page.htm')
    print(article.keys())
    print(article)
