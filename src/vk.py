# -*- coding: utf-8 -*-
import re, os
from settings import user_id, email, password
from network import Network

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
        self.use_tor = False

    def get(self, url, http_type="GET", post={}):
        return Network.get(url, http_type, post)

    def authenticate(self, email, password):
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
    
    def get_dialogs(self,cookie):
        self.headers['Cookie'] = cookie
        dialogs = []
        flag = True
        offset = 0
        while flag:
            data = {
                "act": "a_get_dialogs",
                "al": "1",
                "offset": str(offset),
                "unread": ""
            }
            r,b,c = self.get('http://vk.com/al_im.php',"POST",data)

            a = re.compile("selectDialog\((\d+)\,")
            dialogs.extend(a.findall(b))
            a = re.compile("has_more\"\:true")
            if a.findall(b):
                print "more!", offset
                offset += 20
            else:
                flag = False
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
        r,b,c = self.get('http://vk.com/audio',"POST",data)
        a = re.compile("(http.*?\.mp3)")
        return a.findall(b)

    def download_photo_variants(self, cookie, photo_id, choose_type="all", get_photo=False):
        self.headers['Cookie'] = cookie
        response,body,cookie = self.get("https://vk.com/%s" % photo_id)

        try:
            os.mkdir("photos/%s" % photo_id)
        except:
            pass


        index = body.find("pv_comment")
        index_end = body.find("commcount", index)

        a = re.compile("(\w)_src\"\:\"(.*?)\"")
        imgs = [(img_type, img) for img_type, img in a.findall(body[index:index_end])]
        imgs_types = [img_type for img_type, img in imgs]

        types = ["z", "y", "x", "r", "q", "p", "o"]
        current_type = types[0]
        if choose_type == "max":
            for current_type_2 in types:
                current_type = current_type_2
                if current_type_2 in imgs_types:
                    break
            types = [current_type]

        for img_type, img in imgs:
            if not img_type in types:
                continue
            try:
                response,body,cookie = self.get(img.replace("\\",""))
                if response["status"] == "200":
                    name = img_type + "_src_" +img[-14:]

                    if get_photo:
                        return name, body
                    else:
                        print name
                        with open("photos/%s/%s" % (photo_id, name), 'wb') as f:
                            f.write(body)
            except:
                pass

    def download_photo_album(self, cookie, album_id):
        self.headers['Cookie'] = cookie
        response,body,cookie = self.get("http://vk.com/%s" % album_id)
        r = response
        b = body

        all_photos = []
        # Get amount of images
        a = re.compile("<title>.*?\|.*?(\d+).*</title>")
        try:
            amount = int(a.findall(body)[0])
        except:
            amount = 0

        pageCount = amount / 40 + (amount % 40 != 0)
        a = re.compile("<a\ href=\"(\/photo.*?)\"")
        for i in range(pageCount):
            if (i+1) * 40 < amount:
                print (i+1) * 40, "of", amount
            else:
                print amount, "of", amount

            if i > 0:
                data = {
                    "al": "1",
                    "offset": str( i * 40 ),
                    "part": "1"
                }
                r,b,c = self.get('http://vk.com/%s' % album_id,"POST",data)
            all_photos.extend(a.findall(b))

        print "[test of amount]",  (len(set(all_photos)) == amount)

        try:
            os.mkdir(album_id)
        except:
            pass

        for img in all_photos:
            try:
                print img[1:]
                get_name, get_img = self.download_photo_variants(c, img[1:], "max", get_photo=True)
                with open("%s/%s" % (album_id, get_name), 'wb') as f:
                    f.write(body)
            except:
                pass


        return []



        a = re.compile("<a\ href=\"(\/photo.*?)\"")

        res = a.findall(body)
        n = len(res)

        #res = ['/photo22106310_290082175']

        i = 1
        for img in res:
            r1, b1, c1 = self.get("http://vk.com%s" % img)
            a1 = re.compile("w_src\"\:\"(.*?)\"")
            a2 = re.compile("z_src\"\:\"(.*?)\"")
            res2 = a1.findall(b1)
            res2.extend(a2.findall(b1))

            all_photos.extend(res2)
            print i, "/", n, img
            i += 1

        ph = set(all_photos)
        print len(ph), ph
        try:
            os.mkdir(album_id)
        except:
            pass

        for img in ph:
            try:
                response,body,cookie = self.get(img.replace("\\",""))
                with open(album_id + "/" + img[-14:],'wb') as f:
                    f.write(body)
            except:
                pass

        return ph

if __name__ == "__main__":
    api = vkNApi()
    
    r,b,c = api.authenticate(email,password)
    
    # Получаем список всех диалогов
    #dialogs = api.get_dialogs(c)
    api.download_photo_album(c, "album27053008_000")
    # api.download_photo_variants(c, "photo27053008_291919354", "max")
    print "Exit"


