

'''==================================================================
292. Nim Game
Difficulty: Easy
You are playing the following Nim Game with your friend: There is a heap of stones on the table, each time one of you take turns to remove 1 to 3 stones. The one who removes the last stone will be the winner. You will take the first turn to remove the stones.
Both of you are very clever and have optimal strategies for the game. Write a function to determine whether you can win the game given the number of stones in the heap.
For example, if there are 4 stones in the heap, then you will never win the game: no matter 1, 2, or 3 stones you remove, the last stone will always be removed by your friend.
Hint:
If there are 5 stones in the heap, could you figure out a way to remove the stones such that you will always be the winner?
'''
#Check the number can be devided by 4;
class Solution(object):
    def canWinNim(self, n):
        """
        :type n: int
        :rtype: bool
        """
        if n <= 3:
            return True
        return (n % 4) != 0



'''==================================================================
303. Range Sum Query - Immutable
Difficulty: Easy
Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.
Example:
Given nums = [-2, 0, 3, -5, 2, -1]
sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
Note:
You may assume that the array does not change.
There are many calls to sumRange function.
'''
#DP. Use a array to save sum of numbers. sums[i] means the sum of nums[0]~nums[i]. 
class NumArray(object):
    def __init__(self, nums):
        """
        initialize your data structure here.
        :type nums: List[int]
        """
        sum = 0;
        self.sums = [0] * len(nums);
        for i in range(len(nums)):
            sum += nums[i]
            self.sums[i] = sum

    def sumRange(self, i, j):
        """
        sum of elements nums[i..j], inclusive.
        :type i: int
        :type j: int
        :rtype: int
        """
        if i == 0:
            return self.sums[j]
        else: 
            return self.sums[j] - self.sums[i -1]
# Your NumArray object will be instantiated and called as such:
# numArray = NumArray(nums)
# numArray.sumRange(0, 1)
# numArray.sumRange(1, 2)



'''==================================================================
344. Reverse String
Difficulty: Easy
Write a function that takes a string as input and returns the string reversed.
Example:
Given s = "hello", return "olleh".
'''
#Reverse array.
class Solution(object):
    def reverseString(self, s):
        """
        :type s: str
        :rtype: str
        """
        if s is None:
            return s
        return s[::-1]



'''==================================================================
345. Reverse Vowels of a String
Difficulty: Easy
Write a function that takes a string as input and reverse only the vowels of a string.
Example 1:
Given s = "hello", return "holle".
Example 2:
Given s = "leetcode", return "leotcede".
Note:
The vowels does not include the letter "y".
'''
#Two Pointers. O(n) time. O(n) space.
class Solution(object):
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        VOWELS = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        size = len(s)
        i, j = 0, size - 1
        arr = list(s)
        while i < j:
            while arr[i] not in VOWELS and i < j:
                i += 1
            while arr[j] not in VOWELS and i < j:
                j -= 1
            arr[i], arr[j] = arr[j], arr[i]
            i, j = i + 1, j - 1
        return ''.join(arr)



'''==================================================================
374. Guess Number Higher or Lower
Difficulty: Easy
We are playing the Guess Game. The game is as follows:
I pick a number from 1 to n. You have to guess which number I picked.
Every time you guess wrong, I'll tell you whether the number is higher or lower.
You call a pre-defined API guess(int num) which returns 3 possible results (-1, 1, or 0):
-1 : My number is lower
 1 : My number is higher
 0 : Congrats! You got it!
Example:
n = 10, I pick 6.
Return 6.
'''
# Binary Search! O(logN) time. Be careful with the overflow, use l + (r - l) / 2;
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
# def guess(num):
class Solution(object):
    def guessNumber(self, n):
        """
        :type n: int
        :rtype: int
        """
        l, r, m = 1, n, 0
        while l <= r:
            m = l + (r - l) / 2
            g = guess(m)
            if g == 0:
                break
            elif g == 1:
                l = m + 1
            elif g == -1:
                r = m - 1
        return m



'''==================================================================
383. Ransom Note
Difficulty: Easy
Given an arbitrary ransom note string and another string containing letters from all the magazines, write a function that will return true if the ransom note can be constructed from the magazines;
Each letter in the magazine string can only be used once in your ransom note.
Note:
You may assume that both strings contain only lowercase letters.
canConstruct("a", "b") -> false
canConstruct("aa", "ab") -> false
canConstruct("aa", "aab") -> true
'''
class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        if ransomNote is None:
            return True
        elif magazine is None:
            return False
        arr = [0] * 26
        for c in magazine:
            arr[ord(c) - ord('a')] += 1
        for c in ransomNote:
            if(arr[ord(c) - ord('a')] == 0):
                return False
            else:
                arr[ord(c) - ord('a')] -= 1
        return True