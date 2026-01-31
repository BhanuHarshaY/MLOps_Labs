import unittest
import sys
sys.path.insert(0, 'src')
from string_utils import reverseString, countVowels, convUppercase, isPalindrome

class TestStringUtils(unittest.TestCase):
    def test_reverseString(self):
        self.assertEqual(reverseString("hello"), "olleh")

    def test_countVowels(self):
        self.assertEqual(countVowels("hello"), 2)
        self.assertEqual(countVowels("MLOPs"), 1)

    def test_convUppercase(self):
        self.assertEqual(convUppercase("hello"), "HELLO")

    def test_isPalindrome(self):
        self.assertTrue(isPalindrome("madam"))
        self.assertFalse(isPalindrome("hello"))
        self.assertTrue(isPalindrome("sos"))
        self.assertFalse(isPalindrome("Harsh"))

if __name__ == '__main__':
    unittest.main()
