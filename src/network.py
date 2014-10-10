from TorCtl import TorCtl
import urllib2
import httplib2
import socks
from urllib import urlencode
 
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#httplib2.debuglevel = 4

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.'
            '13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;'
            'q=0.8',
            'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
            'Accept-Charset': 'windows-1251,utf-8;q=1,*;q=0',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

def renew_connection():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="your_password")
    conn.send_signal("NEWNYM")
    conn.close()

def get(url, http_type="GET", post= {}, use_tor=False):
    if use_tor:
        http = httplib2.Http(proxy_info=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, 'localhost', 8118))
    else:
        http = httplib2.Http()

    if http_type == "POST":
        headers["Content-type"] = "application/x-www-form-urlencoded"
        response,body = http.request(url, "POST", urlencode(post), headers=headers)
    else:
        headers["Content-type"] = ''
        response,body = http.request(url, headers=headers)

    if "set-cookie" in response:
        cookie = response["set-cookie"]
    else:
        cookie = ""

    return response, body, cookie