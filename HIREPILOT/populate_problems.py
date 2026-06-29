import os
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prep2Hire.settings')
django.setup()

from judge.models import Problem, TestCase

problems_data = [
    {
        "title": "1. Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0, 1]",
        "testcases": [
            {"input": "[2,7,11,15]\n9", "output": "[0, 1]"},
            {"input": "[3,2,4]\n6", "output": "[1, 2]"},
            {"input": "[3,3]\n6", "output": "[0, 1]"}
        ]
    },
    {
        "title": "2. Reverse String",
        "description": "Write a function that reverses a string. The input string is given as an array of characters s.\n\nExample:\nInput: s = [\"h\",\"e\",\"l\",\"l\",\"o\"]\nOutput: [\"o\",\"l\",\"l\",\"e\",\"h\"]",
        "testcases": [
            {"input": "hello", "output": "olleh"},
            {"input": "world", "output": "dlrow"}
        ]
    },
    {
        "title": "3. Palindrome Number",
        "description": "Given an integer x, return true if x is palindrome integer.\n\nExample:\nInput: x = 121\nOutput: true\nInput: x = -121\nOutput: false",
        "testcases": [
            {"input": "121", "output": "true"},
            {"input": "-121", "output": "false"},
            {"input": "10", "output": "false"}
        ]
    },
    {
        "title": "4. Fibonacci Number",
        "description": "The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1.\n\nExample:\nInput: n = 2\nOutput: 1\nInput: n = 3\nOutput: 2",
        "testcases": [
            {"input": "2", "output": "1"},
            {"input": "3", "output": "2"},
            {"input": "4", "output": "3"}
        ]
    },
    {
        "title": "5. Factorial",
        "description": "Given a positive integer n, return the factorial of n.\n\nExample:\nInput: n = 4\nOutput: 24",
        "testcases": [
            {"input": "4", "output": "24"},
            {"input": "5", "output": "120"}
        ]
    },
    {
        "title": "6. Power of Two",
        "description": "Given an integer n, return true if it is a power of two. Otherwise, return false.\n\nExample:\nInput: n = 1\nOutput: true\nInput: n = 16\nOutput: true",
        "testcases": [
            {"input": "1", "output": "true"},
            {"input": "16", "output": "true"},
            {"input": "3", "output": "false"}
        ]
    },
    {
        "title": "7. Maximum Subarray",
        "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.\n\nExample:\nInput: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6",
        "testcases": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
            {"input": "[1]", "output": "1"},
            {"input": "[5,4,-1,7,8]", "output": "23"}
        ]
    },
    {
        "title": "8. Valid Parentheses",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nExample:\nInput: s = \"()\"\nOutput: true\nInput: s = \"()[]{}\"\nOutput: true",
        "testcases": [
            {"input": "()", "output": "true"},
            {"input": "()[]{}", "output": "true"},
            {"input": "(]", "output": "false"}
        ]
    },
    {
        "title": "9. Climb Stairs",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?\n\nExample:\nInput: n = 2\nOutput: 2",
        "testcases": [
            {"input": "2", "output": "2"},
            {"input": "3", "output": "3"}
        ]
    },
    {
        "title": "10. Single Number",
        "description": "Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.\n\nExample:\nInput: nums = [2,2,1]\nOutput: 1",
        "testcases": [
            {"input": "[2,2,1]", "output": "1"},
            {"input": "[4,1,2,1,2]", "output": "4"}
        ]
    },
    {
        "title": "11. Find Duplicate",
        "description": "Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive. There is only one repeated number in nums, return this repeated number.\n\nExample:\nInput: nums = [1,3,4,2,2]\nOutput: 2",
        "testcases": [
            {"input": "[1,3,4,2,2]", "output": "2"},
            {"input": "[3,1,3,4,2]", "output": "3"}
        ]
    },
    {
        "title": "12. Missing Number",
        "description": "Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.\n\nExample:\nInput: nums = [3,0,1]\nOutput: 2",
        "testcases": [
            {"input": "[3,0,1]", "output": "2"},
            {"input": "[0,1]", "output": "2"}
        ]
    },
    {
        "title": "13. Add Digits",
        "description": "Given an integer num, repeatedly add all its digits until the result has only one digit, and return it.\n\nExample:\nInput: num = 38\nOutput: 2",
        "testcases": [
            {"input": "38", "output": "2"},
            {"input": "0", "output": "0"}
        ]
    },
    {
        "title": "14. Move Zeroes",
        "description": "Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.\n\nExample:\nInput: nums = [0,1,0,3,12]\nOutput: [1,3,12,0,0]",
        "testcases": [
            {"input": "[0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "[0]", "output": "[0]"}
        ]
    },
    {
        "title": "15. Reverse Integer",
        "description": "Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range, then return 0.\n\nExample:\nInput: x = 123\nOutput: 321",
        "testcases": [
            {"input": "123", "output": "321"},
            {"input": "-123", "output": "-321"},
            {"input": "120", "output": "21"}
        ]
    },
    {
        "title": "16. Merge Sorted Arrays",
        "description": "You are given two integer arrays nums1 and nums2, sorted in non-decreasing order. Merge nums2 into nums1 as one sorted array.\n\nExample:\nInput: nums1 = [1,2,3], nums2 = [2,5,6]\nOutput: [1,2,2,3,5,6]",
        "testcases": [
            {"input": "[1,2,3]\n[2,5,6]", "output": "[1,2,2,3,5,6]"},
            {"input": "[1]\n[]", "output": "[1]"}
        ]
    },
    {
        "title": "17. Plus One",
        "description": "You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. Increment the large integer by one and return the resulting array of digits.\n\nExample:\nInput: digits = [1,2,3]\nOutput: [1,2,4]",
        "testcases": [
            {"input": "[1,2,3]", "output": "[1,2,4]"},
            {"input": "[4,3,2,1]", "output": "[4,3,2,2]"},
            {"input": "[9]", "output": "[1,0]"}
        ]
    },
    {
        "title": "18. Length of Last Word",
        "description": "Given a string s consisting of words and spaces, return the length of the last word in the string.\n\nExample:\nInput: s = \"Hello World\"\nOutput: 5",
        "testcases": [
            {"input": "Hello World", "output": "5"},
            {"input": "   fly me   to   the moon  ", "output": "4"}
        ]
    },
    {
        "title": "19. Square Root",
        "description": "Given a non-negative integer x, compute and return the square root of x.\n\nExample:\nInput: x = 4\nOutput: 2",
        "testcases": [
            {"input": "4", "output": "2"},
            {"input": "8", "output": "2"}
        ]
    },
    {
        "title": "20. Check Anagram",
        "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.\n\nExample:\nInput: s = \"anagram\", t = \"nagaram\"\nOutput: true",
        "testcases": [
            {"input": "anagram\nnagaram", "output": "true"},
            {"input": "rat\ncar", "output": "false"}
        ]
    },
    {
        "title": "21. First Unique Character",
        "description": "Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.\n\nExample:\nInput: s = \"leetcode\"\nOutput: 0",
        "testcases": [
            {"input": "leetcode", "output": "0"},
            {"input": "loveleetcode", "output": "2"},
            {"input": "aabb", "output": "-1"}
        ]
    },
    {
        "title": "22. Power of Three",
        "description": "Given an integer n, return true if it is a power of three. Otherwise, return false.\n\nExample:\nInput: n = 27\nOutput: true",
        "testcases": [
            {"input": "27", "output": "true"},
            {"input": "0", "output": "false"},
            {"input": "9", "output": "true"}
        ]
    },
    {
        "title": "23. Number of 1 Bits",
        "description": "Write a function that takes an unsigned integer and returns the number of '1' bits it has (also known as the Hamming weight).\n\nExample:\nInput: n = 11\nOutput: 3",
        "testcases": [
            {"input": "11", "output": "3"},
            {"input": "128", "output": "1"}
        ]
    },
    {
        "title": "24. Majority Element",
        "description": "Given an array nums of size n, return the majority element. The majority element is the element that appears more than ⌊n / 2⌋ times.\n\nExample:\nInput: nums = [3,2,3]\nOutput: 3",
        "testcases": [
            {"input": "[3,2,3]", "output": "3"},
            {"input": "[2,2,1,1,1,2,2]", "output": "2"}
        ]
    },
    {
        "title": "25. Contains Duplicate",
        "description": "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.\n\nExample:\nInput: nums = [1,2,3,1]\nOutput: true",
        "testcases": [
            {"input": "[1,2,3,1]", "output": "true"},
            {"input": "[1,2,3,4]", "output": "false"}
        ]
    },
    {
        "title": "26. Valid Palindrome",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string s, return true if it is a palindrome, or false otherwise.\n\nExample:\nInput: s = \"A man, a plan, a canal: Panama\"\nOutput: true",
        "testcases": [
            {"input": "A man, a plan, a canal: Panama", "output": "true"},
            {"input": "race a car", "output": "false"}
        ]
    },
    {
        "title": "27. Find Difference",
        "description": "You are given two strings s and t. String t is generated by random shuffling string s and then add one more letter at a random position. Return the letter that was added to t.\n\nExample:\nInput: s = \"abcd\", t = \"abcde\"\nOutput: e",
        "testcases": [
            {"input": "abcd\nabcde", "output": "e"},
            {"input": "\ny", "output": "y"}
        ]
    },
    {
        "title": "28. Longest Common Prefix",
        "description": "Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string \"\".\n\nExample:\nInput: strs = [\"flower\",\"flow\",\"flight\"]\nOutput: \"fl\"",
        "testcases": [
            {"input": "[\"flower\",\"flow\",\"flight\"]", "output": "fl"},
            {"input": "[\"dog\",\"racecar\",\"car\"]", "output": ""}
        ]
    },
    {
        "title": "29. Excel Sheet Column Title",
        "description": "Given an integer columnNumber, return its corresponding column title as it appears in an Excel sheet.\n\nExample:\nInput: columnNumber = 1\nOutput: \"A\"\nInput: columnNumber = 28\nOutput: \"AB\"",
        "testcases": [
            {"input": "1", "output": "A"},
            {"input": "28", "output": "AB"},
            {"input": "701", "output": "ZY"}
        ]
    },
    {
        "title": "30. Happy Number",
        "description": "Write an algorithm to determine if a number n is happy. A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat the process until the number equals 1.\n\nExample:\nInput: n = 19\nOutput: true",
        "testcases": [
            {"input": "19", "output": "true"},
            {"input": "2", "output": "false"}
        ]
    },
    {
        "title": "31. Reverse Vowels",
        "description": "Given a string s, reverse only all the vowels in the string and return it.\n\nExample:\nInput: s = \"hello\"\nOutput: \"holle\"",
        "testcases": [
            {"input": "hello", "output": "holle"},
            {"input": "leetcode", "output": "leotcede"}
        ]
    },
    {
        "title": "32. Intersection of Two Arrays",
        "description": "Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique.\n\nExample:\nInput: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2]",
        "testcases": [
            {"input": "[1,2,2,1]\n[2,2]", "output": "[2]"},
            {"input": "[4,9,5]\n[9,4,9,8,4]", "output": "[9,4]"}
        ]
    },
    {
        "title": "33. Ransom Note",
        "description": "Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.\n\nExample:\nInput: ransomNote = \"a\", magazine = \"b\"\nOutput: false",
        "testcases": [
            {"input": "a\nb", "output": "false"},
            {"input": "aa\nab", "output": "false"},
            {"input": "aa\naab", "output": "true"}
        ]
    },
    {
        "title": "34. First Bad Version",
        "description": "You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad. Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one.\n\nExample:\nInput: n = 5, bad = 4\nOutput: 4",
        "testcases": [
            {"input": "5\n4", "output": "4"},
            {"input": "1\n1", "output": "1"}
        ]
    },
    {
        "title": "35. Valid Perfect Square",
        "description": "Given a positive integer num, write a function which returns True if num is a perfect square else False.\n\nExample:\nInput: num = 16\nOutput: true",
        "testcases": [
            {"input": "16", "output": "true"},
            {"input": "14", "output": "false"}
        ]
    },
    {
        "title": "36. Find All Numbers Disappeared in an Array",
        "description": "Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers in the range [1, n] that do not appear in nums.\n\nExample:\nInput: nums = [4,3,2,7,8,2,3,1]\nOutput: [5,6]",
        "testcases": [
            {"input": "[4,3,2,7,8,2,3,1]", "output": "[5,6]"},
            {"input": "[1,1]", "output": "[2]"}
        ]
    },
    {
        "title": "37. Max Consecutive Ones",
        "description": "Given a binary array nums, return the maximum number of consecutive 1's in the array.\n\nExample:\nInput: nums = [1,1,0,1,1,1]\nOutput: 3",
        "testcases": [
            {"input": "[1,1,0,1,1,1]", "output": "3"},
            {"input": "[1,0,1,1,0,1]", "output": "2"}
        ]
    },
    {
        "title": "38. Detect Capital",
        "description": "We define the usage of capitals in a word to be right when one of the following cases holds: All letters in this word are capitals, like \"USA\". All letters in this word are not capitals, like \"leetcode\". Only the first letter in this word is capital, like \"Google\". Given a string word, return true if the usage of capitals in it is right.\n\nExample:\nInput: word = \"USA\"\nOutput: true",
        "testcases": [
            {"input": "USA", "output": "true"},
            {"input": "FlaG", "output": "false"}
        ]
    },
    {
        "title": "39. Student Attendance Record I",
        "description": "You are given a string s representing an attendance record for a student where each character signifies whether the student was absent, late, or present on that day. The record only contains the following three characters: 'A': Absent. 'L': Late. 'P': Present. The student is eligible for an attendance award if they meet both of the following criteria: The student was absent ('A') for strictly fewer than 2 days total. The student was never late ('L') for 3 or more consecutive days. Return true if the student is eligible for an attendance award, or false otherwise.\n\nExample:\nInput: s = \"PPALLP\"\nOutput: true",
        "testcases": [
            {"input": "PPALLP", "output": "true"},
            {"input": "PPALLL", "output": "false"}
        ]
    },
    {
        "title": "40. Reverse Words in a String III",
        "description": "Given a string s, reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.\n\nExample:\nInput: s = \"Let's take LeetCode contest\"\nOutput: \"s'teL ekat edoCteeL tsetnoc\"",
        "testcases": [
            {"input": "Let's take LeetCode contest", "output": "s'teL ekat edoCteeL tsetnoc"},
            {"input": "God Ding", "output": "doG gniD"}
        ]
    },
    {
        "title": "41. Array Partition I",
        "description": "Given an integer array nums of 2n integers, group these integers into n pairs (a1, b1), (a2, b2), ..., (an, bn) such that the sum of min(ai, bi) for all i is maximized. Return the maximized sum.\n\nExample:\nInput: nums = [1,4,3,2]\nOutput: 4",
        "testcases": [
            {"input": "[1,4,3,2]", "output": "4"},
            {"input": "[6,2,6,5,1,2]", "output": "9"}
        ]
    },
    {
        "title": "42. Distribute Candies",
        "description": "Alice has n candies, where the ith candy is of type candyType[i]. Alice noticed that she started to gain weight, so she visited a doctor. The doctor advised Alice to only eat n / 2 of the candies she has. Alice likes her candies very much, and she wants to eat the maximum number of different types of candies while still following the doctor's advice. Given the integer array candyType of length n, return the maximum number of different types of candies she can eat if she only eats n / 2 of them.\n\nExample:\nInput: candyType = [1,1,2,2,3,3]\nOutput: 3",
        "testcases": [
            {"input": "[1,1,2,2,3,3]", "output": "3"},
            {"input": "[1,1,2,3]", "output": "2"}
        ]
    },
    {
        "title": "43. Minimum Index Sum of Two Lists",
        "description": "Suppose Andy and Doris want to choose a restaurant for dinner, and they both have a list of favorite restaurants represented by strings. You need to help them find out their common interest with the least list index sum.\n\nExample:\nInput: list1 = [\"Shogun\",\"Tapioca Express\",\"Burger King\",\"KFC\"], list2 = [\"Piatti\",\"The Grill at Torrey Pines\",\"Hungry Hunter Steakhouse\",\"Shogun\"]\nOutput: [\"Shogun\"]",
        "testcases": [
            {"input": "[\"Shogun\",\"Tapioca Express\",\"Burger King\",\"KFC\"]\n[\"Piatti\",\"The Grill at Torrey Pines\",\"Hungry Hunter Steakhouse\",\"Shogun\"]", "output": "[\"Shogun\"]"},
            {"input": "[\"Shogun\",\"Tapioca Express\",\"Burger King\",\"KFC\"]\n[\"KFC\",\"Shogun\",\"Burger King\"]", "output": "[\"Shogun\"]"}
        ]
    },
    {
        "title": "44. Can Place Flowers",
        "description": "You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots. Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty, and an integer n, return true if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule and false otherwise.\n\nExample:\nInput: flowerbed = [1,0,0,0,1], n = 1\nOutput: true",
        "testcases": [
            {"input": "[1,0,0,0,1]\n1", "output": "true"},
            {"input": "[1,0,0,0,1]\n2", "output": "false"}
        ]
    },
    {
        "title": "45. Set Mismatch",
        "description": "You have a set of integers s, which originally contains all the numbers from 1 to n. Unfortunately, due to some error, one of the numbers in s got duplicated to another number in the set, which results in repetition of one number and loss of another number. You are given an integer array nums representing the data status of this set after the error. Find the number that occurs twice and the number that is missing and return them in the form of an array.\n\nExample:\nInput: nums = [1,2,2,4]\nOutput: [2,3]",
        "testcases": [
            {"input": "[1,2,2,4]", "output": "[2,3]"},
            {"input": "[1,1]", "output": "[1,2]"}
        ]
    },
    {
        "title": "46. Valid Parenthesis String",
        "description": "Given a string s containing only three types of characters: '(', ')' and '*', return true if s is valid.\n\nExample:\nInput: s = \"()\"\nOutput: true\nInput: s = \"(*)\"\nOutput: true",
        "testcases": [
            {"input": "()", "output": "true"},
            {"input": "(*)", "output": "true"},
            {"input": "(*))", "output": "true"}
        ]
    },
    {
        "title": "47. Next Greater Element I",
        "description": "The next greater element of some element x in an array is the first greater element that is to the right of x in the same array. You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2. For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.\n\nExample:\nInput: nums1 = [4,1,2], nums2 = [1,3,4,2]\nOutput: [-1,3,-1]",
        "testcases": [
            {"input": "[4,1,2]\n[1,3,4,2]", "output": "[-1,3,-1]"},
            {"input": "[2,4]\n[1,2,3,4]", "output": "[3,-1]"}
        ]
    },
    {
        "title": "48. Keyboard Row",
        "description": "Given an array of strings words, return the words that can be typed using letters of the alphabet on only one row of American keyboard like the image below. In the American keyboard: the first row consists of the characters \"qwertyuiop\", the second row consists of the characters \"asdfghjkl\", and the third row consists of the characters \"zxcvbnm\".\n\nExample:\nInput: words = [\"Hello\",\"Alaska\",\"Dad\",\"Peace\"]\nOutput: [\"Alaska\",\"Dad\"]",
        "testcases": [
            {"input": "[\"Hello\",\"Alaska\",\"Dad\",\"Peace\"]", "output": "[\"Alaska\",\"Dad\"]"},
            {"input": "[\"omk\"]", "output": "[]"}
        ]
    },
    {
        "title": "49. Relative Ranks",
        "description": "You are given an integer array score of size n, where score[i] is the score of the ith athlete in a competition. All the scores are guaranteed to be unique. The athletes are placed based on their scores, where the 1st place athlete has the highest score, the 2nd place athlete has the 2nd highest score, and so on. The placement of each athlete determines their rank.\n\nExample:\nInput: score = [5,4,3,2,1]\nOutput: [\"Gold Medal\",\"Silver Medal\",\"Bronze Medal\",\"4\",\"5\"]",
        "testcases": [
            {"input": "[5,4,3,2,1]", "output": "[\"Gold Medal\",\"Silver Medal\",\"Bronze Medal\",\"4\",\"5\"]"},
            {"input": "[10,3,8,9,4]", "output": "[\"Gold Medal\",\"5\",\"Bronze Medal\",\"Silver Medal\",\"4\"]"}
        ]
    },
    {
        "title": "50. Perfect Number",
        "description": "A perfect number is a positive integer that is equal to the sum of its positive divisors, excluding the number itself. A divisor of an integer x is an integer that can divide x evenly. Given an integer n, return true if n is a perfect number, otherwise return false.\n\nExample:\nInput: num = 28\nOutput: true",
        "testcases": [
            {"input": "28", "output": "true"},
            {"input": "7", "output": "false"}
        ]
    }
]

created_count = 0
for data in problems_data:
    title = data['title']
    slug = slugify(title)
    
    # Check if problem already exists to avoid duplication
    if not Problem.objects.filter(slug=slug).exists():
        prob = Problem.objects.create(
            title=title,
            slug=slug,
            description=data['description']
        )
        for tc in data['testcases']:
            TestCase.objects.create(
                problem=prob,
                input_data=tc['input'],
                expected_output=tc['output'],
                is_hidden=False
            )
        created_count += 1
        print(f"Created: {title}")
    else:
        print(f"Skipped (already exists): {title}")

print(f"\nSuccessfully added {created_count} new problems.")
