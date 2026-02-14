# Lab 1 - MLOps

This lab covers creating a virtual environment, setting up a GitHub repository, writing Python functions, creating tests using pytest and unittest, and implementing GitHub Actions.

## Folder Structure
```
lab1/
├── src/
│   └── string_utils.py
├── test/
│   ├── test_pytest.py
│   └── test_unittest.py
├── data/
├── requirements.txt
└── README.md
```

## Functions

The string_utils.py file contains the following functions:

- reverseString(s): Reverses a string
- countVowels(s): Counts vowels in a string
- convUppercase(s): Converts string to uppercase
- isPalindrome(s): Checks if string is a palindrome

## Setup

1. Create a virtual environment
```
python3 -m venv lab_01
source lab_01/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

## Running Tests

Pytest:
```
pytest test/test_pytest.py -v
```

Unittest:
```
python3 -m unittest test.test_unittest -v
```

## GitHub Actions

Two workflows are configured:

- pytest_action.yml: Runs pytest on push to main
- unittest_action.yml: Runs unittest on push to main
