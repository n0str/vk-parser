#/usr/bin/python
# -*- coding: utf-8 -*-
from src.scenarios import Scenarios

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

parser.add_argument('--run',
                    dest='run',
                    action='store_const',
                    const=1,
                    help='run default scenario')

result = parser.parse_args()

if result.test:
    testApp()

if result.run:
    runner = Scenarios()
    runner.testScenario()


if True:
    runner = Scenarios()
    runner.testScenario()