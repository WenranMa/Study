
/* ==================================================================
292. Nim Game
Difficulty: Easy
You are playing the following Nim Game with your friend: There is a heap of stones on the table, each time one of you take turns to remove 1 to 3 stones. The one who removes the last stone will be the winner. You will take the first turn to remove the stones.
Both of you are very clever and have optimal strategies for the game. Write a function to determine whether you can win the game given the number of stones in the heap.
For example, if there are 4 stones in the heap, then you will never win the game: no matter 1, 2, or 3 stones you remove, the last stone will always be removed by your friend.
Hint:
If there are 5 stones in the heap, could you figure out a way to remove the stones such that you will always be the winner?
*/
// Check the number can be devided by 4;
public class Solution {
    public boolean canWinNim(int n) {
        if (n <= 3) {
            return true;
        }
        return (n % 4) != 0;
    }
}



/* ==================================================================
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
*/
//DP. Use a array to save sum of numbers. sums[i] means the sum of nums[0]~nums[i]. 
public class NumArray {
    private int[] sums;
    public NumArray(int[] nums) {
        int sum = 0;
        sums = new int[nums.length];
        for(int i = 0; i < nums.length; i++) {
            sum += nums[i];
            sums[i] = sum;
        }
    }
    public int sumRange(int i, int j) {
        return i == 0 ? sums[j] : sums[j] - sums[i - 1];
    }
}
// Your NumArray object will be instantiated and called as such:
// NumArray numArray = new NumArray(nums);
// numArray.sumRange(0, 1);
// numArray.sumRange(1, 2);



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
345. Reverse Vowels of a String
Difficulty: Easy
Write a function that takes a string as input and reverse only the vowels of a string.
Example 1:
Given s = "hello", return "holle".
Example 2:
Given s = "leetcode", return "leotcede".
Note:
The vowels does not include the letter "y".
*/
//Two Pointers. O(n) time. O(n) space.
public class Solution {
    public String reverseVowels(String s) {
        if(s == null || s.length() <= 1) {
            return s;
        }
        char[] arr = s.toCharArray();
        for(int i = 0, j = arr.length - 1; i < j; i++, j--) {
            while(!isVowel(arr[i]) && i < j) {
                i++;
            }
            while(!isVowel(arr[j]) && i < j) {
                j--;
            }
            char temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
        return new String(arr);
    }   
    public boolean isVowel(char c) {
        if(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U' ) {
            return true;
        }
        return false;
    }
}



/* ==================================================================
383. Ransom Note
Difficulty: Easy
Given an arbitrary ransom note string and another string containing letters from all the magazines, write a function that will return true if the ransom note can be constructed from the magazines;
Each letter in the magazine string can only be used once in your ransom note.
Note:
You may assume that both strings contain only lowercase letters.
canConstruct("a", "b") -> false
canConstruct("aa", "ab") -> false
canConstruct("aa", "aab") -> true
*/
//Hash map, O(n) time. O(1) space if there are only 26 characters
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