"""
用户脚本：王孟源的博客
需要提供关键函数：
    get_url_list() - 用于生成所有关注栏目的通知链接

"""
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


def get_date_url_tuple_list(hp):
    '''
    生成所有文章的(日期, 链接)格式列表
    '''
    html = get_url_content(hp)
    date_url_tuple_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find('ul').children:
        if item != '\n' and item.div:
            link = item.a['href']
            link = 'https://taizihuang.github.io/wmyblog' + link[1:] if link.startswith('./') else link
            date = item.div.string
            date_url_tuple_list.append((date, link))

    return date_url_tuple_list


def sort_clip_list(date_url_tuple_list, length=20):
    '''
    将得到的(日期, 链接)列表按日期降序排序，然后截取规定片段长度的前排链接，返回为列表
    '''
    sorted_tuple_list = sorted(date_url_tuple_list, reverse=True)
    url_list = [tpl[1] for tpl in sorted_tuple_list]

    return url_list[:length] if len(url_list) > length else url_list


def get_url_list():
    '''
    生成所有博客文章的链接列表
    '''
    hp = 'https://taizihuang.github.io/wmyblog/'
    date_url_tuple_list = get_date_url_tuple_list(hp)
    url_list = sort_clip_list(date_url_tuple_list)

    return url_list


if __name__ == '__main__':
    url_list = get_url_list()

    for url in url_list:
        print(url)

    import os, sys
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
    import url2article

    print(url2article.parse_article(url))
