
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
299. Bulls and Cows
Difficulty: Easy
You are playing the following Bulls and Cows game with your friend: You write down a number and ask your friend to guess what the number is. Each time your friend makes a guess, you provide a hint that indicates how many digits in said guess match your secret number exactly in both digit and position (called "bulls") and how many digits match the secret number but locate in the wrong position (called "cows"). Your friend will use successive guesses and hints to eventually derive the secret number.
For example:
Secret number:  "1807"
Friend's guess: "7810"
Hint: 1 bull and 3 cows. (The bull is 8, the cows are 0, 1 and 7.)
Write a function to return a hint according to the secret number and friend's guess, use A to indicate the bulls and B to indicate the cows. In the above example, your function should return "1A3B".
Please note that both secret number and friend's guess may contain duplicate digits, for example:
Secret number:  "1123"
Friend's guess: "0111"
In this case, the 1st 1 in friend's guess is a bull, the 2nd or 3rd 1 is a cow, and your function should return "1A1B".
You may assume that the secret number and your friend's guess only contain digits, and their lengths are always equal.
*/
//HashMap. Calculate 'B' first and compare for 'A'. Then B - A. O(n) space, O(n) time.
public class Solution {
    public String getHint(String secret, String guess) {   
        char[] sec = secret.toCharArray();
        char[] gus = guess.toCharArray();
        Map<Character, Integer> map = new HashMap<Character, Integer>();
        int a = 0;
        int b = 0;
        for(char c : sec) {
            if(map.containsKey(c)) {
                map.put(c, map.get(c) + 1);
            } else {
                map.put(c, 1);
            }
        }
        for(char c : gus) {
            if(map.containsKey(c) && map.get(c) > 0) {
                b = b + 1;
                map.put(c, map.get(c) - 1);
            } 
        }
        for(int i = 0; i < sec.length; i++) {
            if(sec[i] == gus[i]) {
                a = a + 1;
            }
        }
        return "" + a + "A" + (b - a) + "B";
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
342. Power of Four
Difficulty: Easy
Given an integer (signed 32 bits), write a function to check whether it is a power of 4.
Example:
Given num = 16, return true. Given num = 5, return false.
Follow up: Could you solve it without loops/recursion?
*/
//Bit Manipulation. Check the num is power of 2, and then check the bits on even number positions is 1. 
public class Solution {
    public boolean isPowerOfFour(int num) {
        return num > 0 && (num & (num -1)) == 0 && (num & 0x55555555) != 0;
    }
}



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
*/
// Binary Search! O(logN) time. Be careful with the overflow, use l + (r - l) / 2;
public class Solution extends GuessGame {
    public int guessNumber(int n) {
        int l = 1;
        int r = n;
        int m = 0;
        while(l <= r) {
            m = l + (r - l) / 2; 
            int g = guess(m);
            if(g == 0) {
                break;
            } else if (g == 1) {
                l = m + 1;
            } else if (g == -1) {
                r = m - 1;
            }
        }
        return m;
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



/* ==================================================================
389. Find the Difference
Difficulty: Easy
Given two strings s and t which consist of only lowercase letters.
String t is generated by random shuffling string s and then add one more letter at a random position.
Find the letter that was added in t.
Example:
Input:
s = "abcd"
t = "abcde"
Output:
e
Explanation:
'e' is the letter that was added.
*/
//Hash Map. O(n) space, O(n) time.
public class Solution {
    public char findTheDifference(String s, String t) {
        Map<Character, Integer> map = new HashMap<Character, Integer>();     
        char[] as = s.toCharArray();
        char[] at = t.toCharArray();    
        char res = ' ';   
        for(char c: as) {
            if(map.containsKey(c)) {
                map.put(c, map.get(c) + 1);
            } else {
                map.put(c, 1);
            }
        }   
        for(char c: at) {
            if(!map.containsKey(c) || map.get(c) == 0) {
                res = c;
            } else {
                map.put(c, map.get(c) - 1); 
            }
        }    
        return res;   
    }
}