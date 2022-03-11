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


if __name__ == '__main__':
    homepage1 = 'http://me.zju.edu.cn/meoffice/'
    url_list1 = get_url_list_tzgg(homepage1)
    print('url_list1 -', len(url_list1), '\n', url_list1)

    homepage2 = 'http://me.zju.edu.cn/meoffice/6440/list.htm'
    url_list2 = get_url_list_yjsjy(homepage2)
    print('url_list2 -', len(url_list2), '\n', url_list2)

    homepage3 = 'http://me.zju.edu.cn/meoffice/6469/list.htm'
    url_list3 = get_url_list_yjsjy(homepage3)
    print('url_list3 -', len(url_list3), '\n', url_list3)
