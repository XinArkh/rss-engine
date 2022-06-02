"""
用户脚本：睡前消息-马前卒工作室
需要提供关键函数：gen_url_list()和parse_article()
"""
import re
import time
import random
import datetime
import platform
import requests
from bs4 import BeautifulSoup


def search_article(homepage, date):
    """在搜狗搜索结果中查看有无所需日期的文章，如有则返回其跳转链接
    """

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    if platform.system() == 'Windows':
        title = '睡前消息【%s】' % date.strftime('%Y-%#m-%#d')
    else:
        title = '睡前消息【%s】' % date.strftime('%Y-%-m-%-d')
    payload = {'type': '2', 'query': title}
    r = requests.get(homepage, params=payload, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    best_title = soup.find('ul', class_='news-list').li.find('div', class_='txt-box').a.text
    if best_title.startswith(title):
        url = 'https://weixin.sogou.com' + \
              soup.find('ul', class_='news-list').li.find('div', class_='txt-box').a['href']
        return url
    else:
        return None


def gen_url_list(homepage, length=10):
    """搜狗搜索-睡前消息
    https://weixin.sogou.com/weixin
    """

    url_list = []
    for l in range(length):
        date = datetime.date.today() - datetime.timedelta(days=l)
        url = search_article(homepage, date)
        if url:
            url_list.append(url)
        time.sleep(0.01)

    return url_list


def parse_url(url, **kwags):
    """解析获取到的搜狗跳转链接，得到公众号推文的永久链接
    参考文章：https://blog.csdn.net/qq_42636010/article/details/94321049
    """

    b = random.randint(0, 99)
    a = url.index('url=')
    a = url[a + 30 + b: a + 31 + b: ]
    url += '&k=' + str(b) + '&h=' + a

    r = requests.get(url, **kwags)
    parsed_url_list = re.findall(r"url \+= '(.+)'", r.text)
    parsed_url = ''.join(parsed_url_list)
    parsed_url = re.sub(r'@', r'', parsed_url)

    if parsed_url == '':
        raise ValueError('parsed URL is empty!')

    return parsed_url


def replace_img_link(html):
    """将推文图片链接转换为外链可以访问的形式
    参考文章：https://blog.csdn.net/yanjiee/article/details/52938144
    """

    return re.sub(r'mmbiz\.qpic\.cn', r'read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=http://mmbiz.qpic.cn', html)


def prettify_article(html):
    """优化文章内容格式"""

    soup = BeautifulSoup(html, 'html.parser')
    soup.p.extract()

    for child in soup.div.children:
        if child.name == 'section' and 'br' in [content.name for content in child.contents]:
            break

        if child.name == 'section':
            previous_sibling = child.previous_sibling
            next_sibling = child.next_sibling
            title = previous_sibling.span.strong.text
            link = next_sibling.span.text

            if re.match(r'\d+\. .*$', title):
                previous_sibling.name = 'h3'
                a_tag = soup.new_tag('a', href=link)
                a_tag.string = title
                previous_sibling.clear()
                previous_sibling.append(a_tag)
            else:
                a_tag = soup.new_tag('a', href=link)
                a_tag.string = '+ ' + title
                previous_sibling.clear()
                previous_sibling.append(a_tag)

            next_sibling.extract()

    html = replace_img_link(str(soup))
    return html


def parse_article(url, **kwags):
    """获取文章信息，并返回对应字典"""
    parsed_url = parse_url(url, **kwags)
    r = requests.get(parsed_url, **kwags)

    import os, sys
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
    import url2article

    article =  url2article.parse_article(parsed_url, **kwags)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    title = soup.h1.text
    title = re.sub(r' |\n', '', title)
    article['title'] = title
    article['content'] = prettify_article(article['content'])

    return article


if __name__ == '__main__':
    homepage = 'https://weixin.sogou.com/weixin'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
               'cookie': 'SUID=0C91AE272208990A000000005C7145DC; SUV=1550927324797555; ssuid=8275997946; LSTMV=241%2C183; LCLKINT=5135; IPLOC=CN3301; weixinIndexVisited=1; ABTEST=0|1654062326|v1; SNUID=67E1DE5770758F331506DFA470A2FCB2; JSESSIONID=aaaSeJsIn-ln9fmk-p6dy; ariaDefaultTheme=undefined'
              }
    url_list = gen_url_list(homepage, length=10)
    
    for url in url_list:
        print(url)

    article = parse_article(url, headers=headers)
    print(article)
    print(article.keys())
