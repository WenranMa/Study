

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
/**
 * @param {number} n
 * @return {boolean}
 */
var canWinNim = function(n) {
    if(!n || n <= 3){
        return true;
    }
    return (n % 4) !== 0;
};



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
/**
 * @constructor
 * @param {number[]} nums
 */
var NumArray = function(nums) {
    this.sums = new Array(nums.length);
    var sum = 0;
    for(var i = 0; i < nums.length; i++) {
        sum += nums[i];
        this.sums[i] = sum;
    }
};
/**
 * @param {number} i
 * @param {number} j
 * @return {number}
 */
NumArray.prototype.sumRange = function(i, j) {
    return i === 0 ? this.sums[j] : this.sums[j] - this.sums[i - 1];
};
/**
 * Your NumArray object will be instantiated and called as such:
 * var numArray = new NumArray(nums);
 * numArray.sumRange(0, 1);
 * numArray.sumRange(0, 2);
 */



/* ==================================================================
344. Reverse String
Difficulty: Easy
Write a function that takes a string as input and returns the string reversed.
Example:
Given s = "hello", return "olleh".
*/
//For loop, O(n) time. O(n) space.
/**
 * @param {string} s
 * @return {string}
 */
var reverseString = function(s) {
    if(!s || s === "") {
        return s;
    }
    var res = "";
    for(var i = s.length; i >= 0; i--) {
        res = res.concat(s.charAt(i));
    }
    return res;
};



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
/**
 * @param {string} s
 * @return {string}
 */
var reverseVowels = function(s) {
    if(!s || s.length <= 1) {
        return s;
    }
    var arr = s.split("");
    for(var i = 0, j = arr.length - 1; i < j; i++, j--) {
        while(!isVowel(arr[i]) && i < j) {
            i++;
        }
        while(!isVowel(arr[j]) && i < j) {
            j--;
        }
        var temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    return arr.join("");
};
var isVowel = function(c) {
    if(c === 'a' || c === 'e' || c === 'i' || c === 'o' || c === 'u' || c === 'A' || c === 'E' || c === 'I' || c === 'O' || c === 'U') {
        return true;
    }
    return false;
};



/* ==================================================================
374. Guess Number Higher or Lower
N/A for JS
*/
// Binary Search! O(logN) time. Be careful with the overflow, use l + (r - l) / 2;



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
/**
 * @param {string} ransomNote
 * @param {string} magazine
 * @return {boolean}
 */
var canConstruct = function(ransomNote, magazine) {
    if(!ransomNote) {
        return true;
    } else if(!magazine) {
        return false;
    }
    var arr = new Array(26);
    for(var i = 0; i < 26; i++) {
        arr[i] = 0;
    }
    for(i = 0; i < magazine.length; i++) {
        arr[magazine[i].charCodeAt() - 97] ++;
    }
    for(i = 0; i < ransomNote.length; i++ ) {
        if(arr[ransomNote[i].charCodeAt() - 97] === 0) {
            return false;
        } else {
            arr[ransomNote[i].charCodeAt() - 97] --;
        }
    }
    return true;
};