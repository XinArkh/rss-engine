import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup


class PiXhost:
    """
    PiXhost image hosting API

    https://pixhost.to/
    """

    def __init__(self):
        self.post_url = 'https://api.pixhost.to/images'
        self.sess_pixhost = requests.session()
        self.sess_pixhost.headers = {
            # 'Content-Type': 'multipart/form-data; charset=utf-8',
            'Accept': 'application/json',
        }
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.sess_pixhost.mount('http://', adapter)
        self.sess_pixhost.mount('https://', adapter)

    def upload_img(self, 
                   img_bin,     # binary image, support formats: gif, png, jpeg
                   # other query parameters, referring to 
                   # https://pixhost.to/api/index.html#images
                   adult=False, # corresponding to content_type, 0 for FS and 1 for NSFW
                   max_th_size=None, 
                   gallery_hash=None, 
                   gallery_upload_hash=None):

        payload = {'content_type': int(adult)}
        if max_th_size:
            payload.update({'max_th_size': max_th_size})
        if gallery_hash:
            payload.update({'gallery_hash': gallery_hash})
        if gallery_upload_hash:
            payload.update({'gallery_upload_hash': gallery_upload_hash})

        file = {
            'img': ('rssengine', img_bin),
        }

        res = self.sess_pixhost.post(self.post_url, data=payload, files=file)
        
        if res.status_code == 200:
            img_url = self.parse_img_url_from_response(res)
        else:
            raise Exception('PiXhost uploading failed! Status code: %d' % res.status_code)

        return img_url

    def parse_img_url_from_response(self, response):
        show_url = response.json()['show_url']
        html = requests.get(show_url).text
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('img', id='image')['src']

        return img_url


if __name__ == '__main__':
    img_bin = requests.get('https://pixhost.to/api/images/logo.png').content

    pix = PiXhost()
    r = pix.upload_img(img_bin)
    print(r)
