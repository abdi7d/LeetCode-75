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