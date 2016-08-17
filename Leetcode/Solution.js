
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