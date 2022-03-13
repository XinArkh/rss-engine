from bs4 import BeautifulSoup
import rss_engine


def fetch_src_list(homepage):
    '''
    研究生院网-信息公告-全部公告
    '''
    html = rss_engine.get_url_content(homepage)
    url_list = []
    title_prefix_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for elem in soup.find_all('div'):
        if elem.get('id') == 'wp_news_w2':
            for item in elem.children:
                if item != '\n':
                    title_prefix_list.append(item.find_all('span')[1].a.string)

                    link = item.find_all('a')[-1].get('href')
                    link = 'http://www.grs.zju.edu.cn' + link if link.startswith('/') else link
                    url_list.append(link)
            break

    return url_list, title_prefix_list


if __name__ == '__main__':
    homepage = 'http://www.grs.zju.edu.cn/'
    url_list, title_prefix_list = fetch_src_list(homepage)
    
    for url, prefix in zip(url_list, title_prefix_list):
        print(prefix, url)
