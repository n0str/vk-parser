# -*- coding: utf-8 -*-

import unittest
from vk import vkNApi
from settings import user_id, email, password

class AllTests(unittest.TestCase):

    def setUp(self, params={}):
        self.Api = vkNApi()
        self.params = {'user_id':user_id, 'email': email, 'password': password}

    def testGet(self):
        self.Api = vkNApi()
        r,b,c = self.Api.get("http://vk.com")
        self.assertEqual(r["status"], '200')

    def testAuth(self):
        api = vkNApi()
        r,b,c = api.authenticate(self.params['email'], self.params['password'])
        self.assertNotIn("Моментальная регистрация", b)

if __name__ == "__main__":
    unittest.main()