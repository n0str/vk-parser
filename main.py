#/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nostr'
import argparse
import unittest

def testApp():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='check.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

parser = argparse.ArgumentParser()
parser.add_argument('--test',
                    dest='test',
                    action='store_const',
                    const=1,
                    help='run unittests')

result = parser.parse_args()

if result.test:
    testApp()