from bs4 import BeautifulSoup
import rss_engine


def get_url_list_tzgg(homepage):
    '''
    《通知公告》板块
    '''
    html = rss_engine.get_url_content(homepage)
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
    html = rss_engine.get_url_content(homepage)
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
    html = rss_engine.get_url_content(homepage)
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


def fetch_src_list(homepage):
    hp1, hp2, hp3 = homepage

    url_list1 = get_url_list_tzgg(hp1)
    url_list2 = get_url_list_yjsjy(hp2)
    url_list3 = get_url_list_xsgz(hp3)

    url_list = url_list1 + url_list2 + url_list3
    title_prefix_list = ['【通知公告】'] * len(url_list1) + ['【研究生教育】'] * len(url_list2) + ['【学生工作】'] * len(url_list3)

    return url_list, title_prefix_list


if __name__ == '__main__':
    homepage1 = 'http://me.zju.edu.cn/meoffice/'
    homepage2 = 'http://me.zju.edu.cn/meoffice/6440/list.htm'
    homepage3 = 'http://me.zju.edu.cn/meoffice/6469/list.htm'

    homepage = [homepage1, homepage2, homepage3]
    url_list, title_prefix_list = fetch_src_list(homepage)

    for url, title_prefix in zip(url_list, title_prefix_list):
        print(title_prefix, url)
