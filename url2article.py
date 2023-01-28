"""
Extract website contents, using URL2io Server by default.
You can also implement custom functions to do so by setting parse_article() in user scripts.

http://url2io.applinzi.com/
"""

import re
import datetime
import requests

from user_api import url2io_token, url2io_api


def get_url_content(url, **kwags):
    """Obtain the source code of the webpage, and return its text"""

    r = requests.get(url, **kwags)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


def parse_article(url, **kwags):
    """Get article information, including link, date, content, and title"""

    html = get_url_content(url, **kwags)
    query_string = {'token': url2io_token, 'url': url,}
    headers_url2io = { 'content-type': "text/html", }
    article = requests.post(url2io_api, params=query_string, headers=headers_url2io, data=html.encode('utf-8'))

    if article.status_code != 200:
        article_info = eval(article.text)
        raise Exception('%s: [Response %d] %s' % (article_info['error'], article.status_code, article_info['msg']))

    article_info = article.json().copy()

    return article_info


if __name__ == '__main__':
    # example
    article = parse_article('https://taizihuang.github.io/wmyblog/html/177266891.html')
    print(article)
    print(article.keys())
