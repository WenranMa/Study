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