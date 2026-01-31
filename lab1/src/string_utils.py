def reverseString(s):
	return s[::-1]

def countVowels(s):
	return sum(1 for c in s.lower() if c in 'aeiou')

def convUppercase(s):
	return s.upper()

def isPalindrome(s):
	cleaned = s.lower().replace(" ", "")
	return cleaned == cleaned[::-1]
