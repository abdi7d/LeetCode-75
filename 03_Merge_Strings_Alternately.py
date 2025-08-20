class Solution:
    def mergeAlternately(self, word1: str, word2:str) ->str:
        merged = []
        i = 0
        # merge charchters alternately while both strings have charctes
        while i < len(word1) or i < len(word2):
            if i < len(word1):
                merged.append(word1[i])
            if i < len(word2):
                merged.append(word2[i])
            i +=1
        return ''.join(merged)

'''
 Time complexity: O(n)
    - where n is the length of the longer string between word1 and word2.
    - the while loop iterates through bothe strings simultaneously and the
      the number of iterations is determined by the maximum length of the two strings.
    - the .join() operation aslo takes O(n) time, making the overall time complexity O(n)

Space complexity: O(n)
   - where n is the length of the longer string. 
   - the space used to store the merged list, which can contain at most n charchters
     (the sum of lengths of word1 and word2), but effectively limited by the longer string due to the alternating pattern
     - the output string also requires O(n) space, so the total space complexity is O(n)
'''
