"""
用户脚本：浙大医学院通知
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


def get_url_list_yltx(homepage):
    '''
    《医路同行》板块
    '''
    html = get_url_content(homepage)
    url_list = []
    title_prefix_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('frag') == '窗口28':      # 重要通知
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【重要通知】')
        elif elem.get('frag') == '窗口29':    # 就业工作
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【就业工作】')
        elif elem.get('frag') == '窗口30':    # 评奖评优
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【评奖评优】')
        elif elem.get('frag') == '窗口31':    # 学生党建
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【学生党建】')
        elif elem.get('frag') == '窗口32':    # 研工动态
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【研工动态】')
        elif elem.get('frag') == '窗口33':    # 政策法规
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【政策法规】')
        elif elem.get('frag') == '窗口34':    # 学生活动
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【学生活动】')
        elif elem.get('frag') == '窗口35':    # 心理指导
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【心理指导】')
        elif elem.get('frag') == '窗口36':    # 表格下载
            for li in elem.find('div', class_='con').ul.find_all('li'):
                link = li.find('span', class_='news_title').a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【表格下载】')

    return url_list, title_prefix_list


def get_url_list_yjsjy(homepage):
    '''
    《研究生教育》板块
    '''
    html = get_url_content(homepage)
    url_list = []
    title_prefix_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('frag') == '窗口13':      # 重点提示
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【重点提示】')
    for elem in soup.find_all('li'):
        if elem.get('frag') == '窗口14':      # 招生信息
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【招生信息】')
        elif elem.get('frag') == '窗口15':    # 学籍及资助
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【学籍及资助】')
        elif elem.get('frag') == '窗口24':    # 培养管理
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【培养管理】')
        elif elem.get('frag') == '窗口25':    # 学位管理
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【学位管理】')
        elif elem.get('frag') == '窗口34':    # 学科及导师
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【学科及导师】')
        elif elem.get('frag') == '窗口35':    # 公派出国
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【公派出国】')
        elif elem.get('frag') == '窗口44':    # 同等学力
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【同等学力】')
        elif elem.get('frag') == '窗口45':    # 工作文件
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【工作文件】')
        elif elem.get('frag') == '窗口54':    # 相关下载
            for li in elem.ul.find_all('li'):
                link = li.a['href']
                link = 'http://www.cmm.zju.edu.cn' + link if link.startswith('/') else link
                url_list.append(link)
                title_prefix_list.append('【相关下载】')

    return url_list, title_prefix_list


def gen_url_list(homepage):
    hp1, hp2 = homepage

    url_list1, title_prefix_list1 = get_url_list_yltx(hp1)
    url_list2, title_prefix_list2 = get_url_list_yjsjy(hp2)

    url_list = url_list1 + url_list2
    title_prefix_list = ['【医路同行】'+prefix for prefix in title_prefix_list1] + ['【研究生教育】'+prefix for prefix in title_prefix_list2]

    # 剔除非网页链接（doc, pdf）
    url_list_new = []
    title_prefix_list_new = []
    for i in range(len(url_list)):
        if url_list[i].endswith('htm') or url_list[i].endswith('html'):
            url_list_new.append(url_list[i])
            title_prefix_list_new.append(title_prefix_list[i])

    return url_list_new, title_prefix_list_new
    # return url_list, title_prefix_list


def match_pubdate(html):
    '''
    尝试在html文本中匹配【发布日期】片段，若匹配到则将其作为发布时间返回
    p.s. api自带的时间提取功能错误率比较高，经常把正文中的时间提取为发表时间
    '''
    searchObj = re.search(r'发布日期：[0-9]{4}年[0-9]{2}月[0-9]{2}日 [0-9]{1,2}:[0-9]{2}', html)

    if searchObj:
        pubdate = datetime.datetime.strptime(searchObj.group(0)[5:], '%Y年%m月%d日 %H:%M')
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
    homepage1 = 'http://www.cmm.zju.edu.cn/yltx/list.htm'   # 医路同行
    homepage2 = 'http://www.cmm.zju.edu.cn/38700/list.htm'  # 研究生教育

    homepage = [homepage1, homepage2]
    url_list, title_prefix_list = gen_url_list(homepage)

    for url, title_prefix in zip(url_list, title_prefix_list):
        print(title_prefix, url)

    article = parse_article('http://www.cmm.zju.edu.cn/2022/0613/c38818a2591359/page.htm')
    print(article)
    print(article.keys())
