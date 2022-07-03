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

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    if platform.system() == 'Windows':
        title = '睡前消息【%s】' % date.strftime('%Y-%#m-%#d')
    else:
        title = '睡前消息【%s】' % date.strftime('%Y-%-m-%-d')
    payload = {'type': '2', 'query': title}
    r = requests.get(homepage, params=payload, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    url = None
    if not soup.find('ul', class_='news-list'):
        raise Exception('Sogou search error!')
    for news in soup.find('ul', class_='news-list'):
        if not news.name == 'li':
            continue
        if news.find('div', class_='txt-box').a.text.startswith(title):
            url = 'https://weixin.sogou.com' + news.find('div', class_='txt-box').a['href']
            break

    return url


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
        time.sleep(0.1)

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
    """

    # 方法一：https://blog.csdn.net/yanjiee/article/details/52938144
    # return re.sub(r'mmbiz\.qpic\.cn', 
    #               r'read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=http://mmbiz.qpic.cn', 
    #               html
    #               )
    # 方法二：https://bjun.tech/blog/xphp/31
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        img['referrerpolicy'] = 'same-origin'
    return str(soup)


def remove_break_line(html):
    """移除网页源代码中的空白行"""

    return re.sub(r'<p>(<(span|strong)>)*?(<br/?>|　| | )(<(/span|/strong)>)*?</p>',
                  r'', 
                  html
                  )


def prettify_article(html):
    """优化文章内容格式"""

    html = replace_img_link(html)
    html = remove_break_line(html)

    soup = BeautifulSoup(html, 'html.parser')
    if soup.p.img:                                          # 去除置顶的关注引导图片
        soup.p.clear()

    for child in soup.div.children:
        if child.get_text().startswith('长按或扫码') or child.get_text().startswith('欢迎点击'):
            p_tag = soup.new_tag('p')
            br_tag = soup.new_tag('br')
            p_tag.append(br_tag)
            child.insert_before(p_tag)
            break

        if child.name == 'p' or str(child.name).startswith('h'):
            if child.get_text():
                if not child.get_text().startswith('http'): # child为文本，包括带数字的大标题或不带数字的小标题
                    title = child.get_text()
                    if re.match(r'\d+\..*$', title):        # 如果是大标题，预先将其标签改为<h3>
                        child.name='h3'
                    else:                                   # 如果是小标题
                        if not child.name == 'p':           # 如果其标签不是<p>，则将其转化为<p>
                            child.name = 'p'
                        if str(child.previous_sibling) == '<p><br/></p>':  # 如果前面是空行（转化自上一条新闻的链接标签），将其去除
                            child.previous_sibling.clear()
                        # 如果不是空行，说明上一条目没有链接，不需要再去除
                    prev_sibling = child
                else:                                       # child为链接
                    link = child.get_text()
                    link = re.sub(r' ', r'', link)     # 去除链接末尾的 

                    if re.match(r'\d+\..*$', title):        # 判断前面的元素为大标题，为其增加超链接
                        a_tag = soup.new_tag('a', href=link)
                        a_tag.string = title
                        prev_sibling.clear()
                        prev_sibling.append(a_tag)
                    else:                                   # 判断前面元素非大标题，可能是小标题或根本没有小标题
                        a_tag = soup.new_tag('a', href=link)
                        a_tag.string = '+ ' + title
                        if title != '':                     # 有小标题，为其添加超链接
                            prev_sibling.clear()
                            prev_sibling.append(a_tag)
                        else:                               # 无小标题，将前面残余的空行（转化自上一条新闻的链接标签）转换为超链接小标题
                            assert str(child.previous_sibling.previous_sibling) == '<p><br/></p>'
                            child.previous_sibling.previous_sibling.clear()
                            child.previous_sibling.previous_sibling.append(a_tag)

                    child.clear()                       # 将原本的链接<p>标签转换为话题间的空行
                    br_tag = soup.new_tag('br')
                    child.append(br_tag)

                    title = ''                              # 经过一个链接后，将标题和标签数据清空
                    prev_sibling = None

    return str(soup)


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

    article = parse_article(url_list[0], headers=headers)
    print(article)
    print(article.keys())
