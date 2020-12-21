import unittest
from python_ledbox.TestClass import TestClass


class TestTestClass(unittest.TestCase):
    def setUp(self):
        self.test_obj = TestClass()

    def test_add_integers(self):
        self.assertEqual(4, self.test_obj.add_integers(1, 3))

    def test_abs(self):
        self.assertEqual(3, self.test_obj.abs(3))
        self.assertEqual(3, self.test_obj.abs(-3))
