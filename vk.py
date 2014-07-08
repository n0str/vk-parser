# -*- coding: utf-8 -*-
import httplib2, re
from urllib import urlencode
from settings import user_id, email, password

class vkNApi():
    profile = 0
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.'
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

    def __init__(self):
        pass

    def get(self, url, http_type="GET", post={}):
        Http = httplib2.Http()
        if http_type == "POST":
            self.headers["Content-type"] = "application/x-www-form-urlencoded"
            response,body = Http.request(url, "POST", urlencode(post), headers=self.headers)
        else:
            self.headers["Content-type"] = ''
            response,body = Http.request(url, headers=self.headers)

        if "set-cookie" in response:
            cookie = response["set-cookie"]
        else:
            cookie = ""

        return response, body, cookie

    def authenticate(self, email, password):
        Http = httplib2.Http()

        # Загружаем главную страницу для получения cookie
        response, body, cookie = self.get("http://vk.com")
        self.headers['Cookie'] = cookie

        # Получаем ip_h
        a = re.compile("ip_h\"\ value=\"([a-zA-Z0-9]+)")
        ip_h = a.findall(body)[0]

        # Формируем данные для post запроса
        post = {
            'act':"login",
            'role':"al_frame",
            'email':email,
            'pass':password,
            'ip_h':ip_h,
            '_origin': "http://vk.com",
            'expire': '',
            'captcha_sid': '',
            'captcha_key': '',
        }

        # Аутентификация
        response,body,cookie = self.get("http://login.vk.com/?act=login","POST", post)
        self.headers['Cookie'] = cookie

        # Получаем remixsid
        response,body,cookie = self.get(response["location"])
        a = re.compile("(remixsid=[a-f0-9]+)")
        rsid = a.findall(cookie)

        # Формируем рабочие headers
        self.headers['Cookie'] = "remixlang=0; remixflash=14.0.0; remixscreen_depth=24; remixdt=14400; " + rsid[0]
        
        response,body,cookie = self.get("http://vk.com/")
        
        return response,body,self.headers['Cookie']
    
    def get_dialogs(self,cookie, quantity = -1):
        self.headers['Cookie'] = cookie
        dialogs = []
        flag = True
        offset = 0
        while flag and quantity != 0:
            data = {
                "act": "a_get_dialogs",
                "al": "1",
                "offset": str(offset),
                "unread": ""
            }
            r,b,c = api.get('http://vk.com/al_im.php',"POST",data)

            a = re.compile("selectDialog\((\d+)\,")
            dialogs.extend(a.findall(b))
            a = re.compile("has_more\"\:true")
            if a.findall(b):
                print "more!", offset
                offset += 20
            else:
                flag = False
            quantity -= 1
        return list(set(dialogs))

    def get_audio(self, cookie):
        self.headers['Cookie'] = cookie
        data = {
            'act':'load_audios_silent',
            'al':'1',
            'gid':'0',
            'id':user_id,
            'please_dont_ddos':'2'
        }
        r,b,c = api.get('http://vk.com/audio',"POST",data)
        a = re.compile("(http.*?\.mp3)")
        return a.findall(b)

if __name__ == "__main__":
    api = vkNApi()
    
    r,b,c = api.authenticate(email,password)

    # Получаем список всех диалогов
    dialogs = api.get_dialogs(c,10)




