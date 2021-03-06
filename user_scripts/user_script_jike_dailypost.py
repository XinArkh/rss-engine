"""
用户脚本：即刻App-一觉醒来世界发生了什么
需要提供关键函数：gen_url_list()和parse_article()
"""
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
    即刻App-一觉醒来世界发生了什么
    https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68
    '''
    html = get_url_content(homepage)
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for li in soup.find('ul', class_='post-list'):
        # print(li.find('div', class_='jsx-3930310120').find('a')['href'])
        url_list.append(li.find('div', class_='jsx-3930310120').find('a')['href'])

    return url_list


def parse_article(url):
    article = {}
    article['url'] = url

    html = get_url_content(url)
    soup = BeautifulSoup(html, 'html.parser')

    article['title'] = soup.title.text
    article['date'] = str(datetime.datetime.strptime(article['title'][:8], '%Y%m%d'))

    content = ''
    for li in soup.find('ul', class_='main'):
        link = li.a['href']
        num = li.find('span', class_='num').text
        text = li.find('span', class_='text').text
        content += '<a href="%s">%s %s</a><br>' % (link, num, text)
    article['content'] = content

    return article


if __name__ == '__main__':
    homepage = 'https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68'
    url_list = gen_url_list(homepage)
    
    for url in url_list:
        print(url)

    article = parse_article(url_list[0])
    print(article)
    print(article.keys())
