class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        s_ptr = 0
        t_ptr = 0
        
        while s_ptr < len(s) and t_ptr < len(t):
            if s[s_ptr] == t[t_ptr]:
                s_ptr += 1
            t_ptr += 1
            
        return s_ptr == len(s)

# Time Complexity: O(n) where n = len(t) (because t is always scanned fully or almost fully)

 # Space Complexity: O(1) constant extra space)