# Lab 04: Loops and Functions Practice
# Student Name: Maziar Sojoudian
# Date: Feb 06, 2026

# ==================================================
# Question 1: Robot Return to Origin
# ==================================================

print("\n" + "=" * 50)
print("Question 1: Robot Return to Origin")
print("=" * 50)

def robot_returns_to_origin(moves):  # ["UD", "LL", "UDLR", "LDRRLUULR"]
    # Initialize starting position
    x = 0
    y = 0

    # Loop through each move and update x, y
    for move in moves:
        if move == "U":
            y = y + 1  # y += 1
        elif move == "D":
            y = y - 1  # y -= 1
        elif move == "R":
            x = x + 1  # x += 1
        elif move == "L":
            x = x - 1  # x -= 1

    # Return True if back at origin, False otherwise
    return x ==0 and y==0

# Test cases
test_moves = ["UD", "LL", "UDLR", "LDRRLUULR"]

for moves in test_moves:
    result = robot_returns_to_origin(moves)
    print("Moves '" + moves + "': Returns to origin? " + str(result))

# ==================================================
# Question 2: Two Sum
# ==================================================
# Part A: Brute Force with Nested Loops

def two_sum_brute_force(numbers, target):
    # Use nested loops to find the pair
    # Outer loop: i from 0 to len(numbers)
    for i in range(len(numbers)):
        # Inner loop: j from i+1 to len(numbers)
        for j in range(i+1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return (i, j)
    return None


# Part B: Optimized with Dictionary
def two_sum_optimized(numbers, target):
    seen = {}  # Dictionary to store {number: index}
    # Loop through numbers, check if needed value exists in seen
    for i in range(len(numbers)):
        needed = target - numbers[i]
        if needed in seen:
            return (seen[needed], i)
        seen[numbers[i]] = i
    return None


# ==================================================
# Question 3: Shuffle the Array
# ==================================================

# ==================================================
# Question 4: First Unique Character
# ==================================================
