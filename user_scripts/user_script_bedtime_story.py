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


def fetch_src_list(homepage, length=10):
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


def parse_url(url, headers):
    """解析获取到的搜狗跳转链接，得到公众号推文的永久链接
    参考文章：https://blog.csdn.net/qq_42636010/article/details/94321049
    """

    b = random.randint(0, 99)
    a = url.index('url=')
    a = url[a + 30 + b: a + 31 + b: ]
    url += '&k=' + str(b) + '&h=' + a

    r = requests.get(url, headers=headers)
    parsed_url_list = re.findall(r"url \+= '(.+)'", r.text)
    parsed_url = ''.join(parsed_url_list)
    parsed_url = re.sub(r'@', r'', parsed_url)

    if parsed_url == '':
        raise ValueError('parsed URL is empty!')

    return parsed_url


def get_article(url, headers=None):
    """获取文章信息，并返回对应字典"""

    parsed_url = parse_url(url, headers)
    r = requests.get(parsed_url, headers=headers)

    import os, sys
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
    from url2article import get_article

    article =  get_article(parsed_url, headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.h1.text
    title = re.sub(r' |\n', '', title)
    article['title'] = title

    return article


if __name__ == '__main__':
    homepage = 'https://weixin.sogou.com/weixin'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
               'cookie': 'SUID=0C91AE272208990A000000005C7145DC; SUV=1550927324797555; ssuid=8275997946; LSTMV=241%2C183; LCLKINT=5135; IPLOC=CN3301; weixinIndexVisited=1; ABTEST=0|1654062326|v1; SNUID=67E1DE5770758F331506DFA470A2FCB2; JSESSIONID=aaaSeJsIn-ln9fmk-p6dy; ariaDefaultTheme=undefined'
              }
    url_list = fetch_src_list(homepage, length=10)
    
    for url in url_list:
        print(url)

    article = get_article('https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS1ZM0G5Td09PKUcZzsf1jTd9lGUZ_6mPSFqXa8Fplpd9t7Q0oQJXYSXuh6mnsFCHNaGEv31tEijR9OjNVsc24d0dZrR4C_ixT4d9g8XiZE1tqLuBlC81DQKu53CDnyhOFp-8Q3pbZ17Uo_oZ-B_LSunlzZ_Hyaak9Ed-YWbgs8uj1lRQ62xC32Z4umJeZekRNSzNo7E-E9BAsTrrQp4bVwwNGbbB75bUeA..&type=2&query=%E7%9D%A1%E5%89%8D%E6%B6%88%E6%81%AF%E3%80%902022-5-31%E3%80%91&token=2D86DADEA7201E96B1B450D3176A8F42B16C5DB8629765FB', 
                          headers)
    print(article)
    print(article.keys())
