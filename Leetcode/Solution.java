
/* ==================================================================
344. Reverse String
Difficulty: Easy
Write a function that takes a string as input and returns the string reversed.

Example:
Given s = "hello", return "olleh".
*/
//For loop, O(n) time. O(n) space.
public class Solution {
    public String reverseString(String s) {
        if(s == null || s.length() == 0) {
            return s;
        }
        StringBuilder res = new StringBuilder();
        for(int i = s.length() - 1; i >= 0; i--) {
            res.append(s.charAt(i));
        }
        return res.toString();
    }
}


/* ==================================================================
383. Ransom Note
Difficulty: Easy
 Given  an  arbitrary  ransom  note  string  and  another  string  containing  letters from  all  the  magazines,  write  a  function  that  will  return  true  if  the  ransom   note  can  be  constructed  from  the  magazines ;  otherwise,  it  will  return  false.   
Each  letter  in  the  magazine  string  can  only  be  used  once  in  your  ransom  note.

Note:
You may assume that both strings contain only lowercase letters.
canConstruct("a", "b") -> false
canConstruct("aa", "ab") -> false
canConstruct("aa", "aab") -> true
*/
//Hash map, O(n) time. O(1) space if there are only 26 character.s
public class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        
        if(ransomNote == null || ransomNote.length() == 0) {
            return true;
        } else if(magazine == null || magazine.length() == 0) {
            return false;
        }
        
        Map<Character, Integer> map = new HashMap<Character, Integer>();
        
        for(int i = 0; i< magazine.length(); i++){
            char c = magazine.charAt(i);
            if(map.containsKey(c)) {
                map.put(c, map.get(c) + 1);
            } else {
                map.put(c, 1);
            }
        }
        
        for(int i = 0; i< ransomNote.length(); i++){
            char c = ransomNote.charAt(i);
            if(!map.containsKey(c) || map.get(c) <= 0){
                return false;
            } else {
                map.put(c, map.get(c) - 1);
            }
        }
        
        return true;
    }
}