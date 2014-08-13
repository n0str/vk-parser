import unittest
from vk import vkNApi

class AllTests(unittest.TestCase):

    def setUp(self):
        self.Api = vkNApi()

    def testGet(self):
        self.Api = vkNApi()
        r,b,c = self.Api.get("http://vk.com")
        self.assertEqual(r["status"], '200')

if __name__ == "__main__":
    unittest.main()