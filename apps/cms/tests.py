from django.test import TestCase

# Create your tests here.

import unittest

class TestObject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('start' + '+'*100)

    @classmethod
    def tearDownClass(cls) -> None:
        print('end' + '+'*100)


    def setUp(self):
        print('开始')

    def tearDown(self) -> None:
        print('结束')


    def test_a(self):
        self.assertEqual(1, 1)

    def test_b(self):
        self.assertEqual(2, 1)

if __name__ == '__main__':
    unittest.main()


