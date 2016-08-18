

''' ==================================================================
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
            return True;
        return (n % 4) != 0;



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
383. Ransom Note
Difficulty: Easy
 Given  an  arbitrary  ransom  note  string  and  another  string  containing  letters from  all  the  magazines,  write  a  function  that  will  return  true  if  the  ransom   note  can  be  constructed  from  the  magazines ;  otherwise,  it  will  return  false.   
Each  letter  in  the  magazine  string  can  only  be  used  once  in  your  ransom  note.

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
            return True;
        elif magazine is None:
            return False;
        arr = [0] * 26;
        for c in magazine:
            arr[ord(c) - ord('a')] += 1;
        for c in ransomNote:
            if(arr[ord(c) - ord('a')] == 0):
                return False;
            else:
                arr[ord(c) - ord('a')] -= 1;
        return True;