# main_program.py

# Import the custom module
import my_utils

# Import standard library modules
import math
import random

# Call the greet function
my_utils.greet("Alice")

# Test the is_prime function
print("Is 7 prime?", my_utils.is_prime(7))
print("Is 10 prime?", my_utils.is_prime(10))

# Calculate the square root
number = 25
print("Square root of", number, "is", math.sqrt(number))

# Generate a random number between 1 and 100
random_number = random.randint(1, 100)
print("Random number:", random_number)
