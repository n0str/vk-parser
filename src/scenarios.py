# -*- coding: utf-8 -*-

from vk import vkNApi
from settings import user_id, email, password, network_defaults

class Scenarios():

    def testScenario(self):
        api = vkNApi()

        r,b,c = api.authenticate(email,password)

        api.download_photo_album(c, "album27053008_000")
        api.download_photo_variants(c, "photo27053008_291919354", "max")
        print "Exit"