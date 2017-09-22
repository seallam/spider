import re
import json
from bs4 import BeautifulSoup
from urllib import  request, parse

if __name__ == '__main__':
    ip = "http://www.iqiyi.com/v_19rr8ykarc.html"
    get_url = 'http://www.sfsft.com/index.php?url=%s' % ip
    get_video_url = 'http://www.sfsft.com/api.php'

    head = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
        'Referer': 'http://www.sfsft.com/index.php?url=%s' % ip
    }

    get_url_req = request.Request(url=get_url, headers=head)
    get_url_response = request.urlopen(get_url_req)
    get_url_html = get_url_response.read().decode('utf-8')
    soup = BeautifulSoup(get_url_html, 'lxml')

    a = str(soup.find_all('script'))

    partten = re.compile("url : '(.+)',", re.IGNORECASE)
    url = partten.findall(a)[0]

    get_video_data = {
        'up':'0',
        "url":'%s' % url
    }

    get_video_req = request.Request(url=get_video_url, headers=head)
    get_video_data = parse.urlencode(get_video_data).encode('utf-8')
    get_video_response = request.urlopen(get_video_req, get_video_data)
    get_video_html = get_video_response.read().decode('utf-8')
    print(get_video_data['url'])
