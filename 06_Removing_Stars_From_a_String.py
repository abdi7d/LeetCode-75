class Solution:
    def removeStars(self, s: str) -> str:
        stack = []
        for ch in s:
            if ch =="*":
                stack.pop() #remove the closest left character
            else:
                stack.append(ch)
        return ''.join(stack)

# Time Complexity: O(n) (each char is processed once)
# Space Complexity: O(n) (Stack stores result)