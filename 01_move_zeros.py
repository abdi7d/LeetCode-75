class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        # First pointer: Pointer to place the next non-zero element(position to place the next non-zero element)
        last_non_zero = 0

        # Second pointer: scan the list (Move non-zeroes forward)
        for i in range(len(nums)):
            if nums[i] != 0:
                # Swap current non-zero with last_non_zero
                nums[last_non_zero], nums[i] = nums[i], nums[last_non_zero]
                last_non_zero += 1
# Time Complexity: O(n)
    
# Space Complexity: O(1) → in-place, no extra list used