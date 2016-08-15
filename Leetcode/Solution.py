



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