import sys
sys.path.insert(0, 'src')
from string_utils import reverseString, countVowels, convUppercase, isPalindrome

def test_reverseString():
    assert reverseString("hello") == "olleh"

def test_countVowels():
    assert countVowels("hello") == 2

def test_convUppercase():
    assert convUppercase("hello") == "HELLO"

def test_isPalindrome():
    assert isPalindrome("madam") == True
    assert isPalindrome("hello") == False
