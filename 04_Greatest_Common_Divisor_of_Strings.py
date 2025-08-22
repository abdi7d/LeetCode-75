class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # If concatening str1 and str2 is not equal to str2 and str1, no common divisor exists
        if str1 + str2 != str2 + str1:
            return ""
        
        # GCD of lengths gives the maximum possible length of common divisor
        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a
        
