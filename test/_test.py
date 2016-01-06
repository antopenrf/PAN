import unittest
from rwg import *

class _TestBase(unittest.TestCase):
    def _testEqual(self, tobeTest, answers):
        print('\nTesting ' + self.__class__.__name__)
        for index, each in enumerate(answers):
            self.assertEqual(each, tobeTest[index])

    def _testCloseEnough(self, tobeTest, answers, tolerance = 10):
        print('\nTesting ' + self.__class__.__name__)
        for index, each in enumerate(answers):
            tester = tobeTest[index]
            self.assertLess(abs(each - tester), tolerance)

