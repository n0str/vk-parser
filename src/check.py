# -*- coding: utf-8 -*-

import unittest
from vk import vkNApi
from settings import user_id, email, password, network_defaults

class AllTests(unittest.TestCase):

    def setUp(self, params={}):
        self.Api = vkNApi()
        self.params = {'user_id':user_id, 'email': email, 'password': password}

    def testGet(self):
        self.Api = vkNApi()
        r,b,c = self.Api.get("http://vk.com")
        self.assertEqual(r["status"], '200')

    def test_ip_address(self):
        self.api = vkNApi()

        # If you want to use hidden network
        network_defaults['use_tor'] = True
        r,b,c = self.api.get("http://icanhazip.com/")

        self.assertEqual(r["status"], '200')
        print "[TOR_IP_ADDRESS]", b

    def testAuth(self):
        api = vkNApi()
        r,b,c = api.authenticate(self.params['email'], self.params['password'])
        self.assertNotIn("Моментальная регистрация", b)

if __name__ == "__main__":
    unittest.main()