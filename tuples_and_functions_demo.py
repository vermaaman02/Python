"""
Python Tuples and Functions Demonstration
=========================================

This file demonstrates the key concepts of tuples and functions in Python.
"""

print("=" * 50)
print("TUPLES DEMONSTRATION")
print("=" * 50)

# 1. Creating different types of tuples
print("\n1. Creating Tuples:")
coordinates = (10, 20)
print(f"Coordinates: {coordinates}")

colors = ("red", "green", "blue", "yellow")
print(f"Colors: {colors}")

mixed_data = (1, "Python", 3.14, True, [1, 2, 3])
print(f"Mixed data: {mixed_data}")

empty_tuple = ()
print(f"Empty tuple: {empty_tuple}")

single_item = (42,)  # Comma is important!
print(f"Single item tuple: {single_item}")

# 2. Accessing tuple elements
print("\n2. Accessing Tuple Elements:")
print(f"First color: {colors[0]}")
print(f"Last color: {colors[-1]}")
print(f"First two colors: {colors[0:2]}")

# 3. Tuple operations
print("\n3. Tuple Operations:")
print(f"Length of colors tuple: {len(colors)}")
print(f"Count of 'red' in colors: {colors.count('red')}")
print(f"Index of 'blue': {colors.index('blue')}")

# 4. Tuple unpacking
print("\n4. Tuple Unpacking:")
x, y = coordinates
print(f"x = {x}, y = {y}")

first, *middle, last = colors
print(f"First: {first}, Middle: {middle}, Last: {last}")

# 5. Tuples are immutable
print("\n5. Immutability:")
print("Tuples cannot be modified after creation!")
# colors[0] = "purple"  # This would cause an error!

# 6. Nested tuples
print("\n6. Nested Tuples:")
nested = ((1, 2), (3, 4), (5, 6))
print(f"Nested tuple: {nested}")
print(f"First inner tuple: {nested[0]}")
print(f"Element from nested tuple: {nested[1][0]}")

print("\n" + "=" * 50)
print("FUNCTIONS DEMONSTRATION")
print("=" * 50)

# 1. Basic function definition
def greet():
    """A simple function that prints a greeting."""
    print("Hello, Python World!")

print("\n1. Basic Function:")
greet()

# 2. Function with parameters
def greet_person(name):
    """Function that greets a specific person."""
    print(f"Hello, {name}!")

print("\n2. Function with Parameters:")
greet_person("Alice")
greet_person("Bob")

# 3. Function with return value
def add_numbers(a, b):
    """Function that adds two numbers and returns the result."""
    return a + b

print("\n3. Function with Return Value:")
result = add_numbers(5, 3)
print(f"5 + 3 = {result}")

# 4. Function with default parameters
def introduce(name, age=25, city="Unknown"):
    """Function with default parameter values."""
    return f"Hi, I'm {name}, {age} years old, from {city}."

print("\n4. Function with Default Parameters:")
print(introduce("Charlie"))
print(introduce("Diana", 30))
print(introduce("Eve", 28, "New York"))

# 5. Function with variable arguments (*args)
def sum_all(*numbers):
    """Function that sums any number of arguments."""
    total = 0
    for num in numbers:
        total += num
    return total

print("\n5. Function with Variable Arguments (*args):")
print(f"Sum of 1, 2, 3: {sum_all(1, 2, 3)}")
print(f"Sum of 1, 2, 3, 4, 5: {sum_all(1, 2, 3, 4, 5)}")

# 6. Function with keyword arguments (**kwargs)
def create_profile(**details):
    """Function that creates a profile from keyword arguments."""
    profile = "Profile: "
    for key, value in details.items():
        profile += f"{key}={value}, "
    return profile.rstrip(", ")

print("\n6. Function with Keyword Arguments (**kwargs):")
print(create_profile(name="Frank", age=35, job="Engineer"))
print(create_profile(name="Grace", city="Boston", hobby="Reading"))

# 7. Functions working with tuples
def get_coordinates():
    """Function that returns a tuple."""
    return (100, 200)

def calculate_distance(point1, point2):
    """Function that calculates distance between two points (tuples)."""
    x1, y1 = point1
    x2, y2 = point2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

print("\n7. Functions Working with Tuples:")
point_a = get_coordinates()
point_b = (150, 250)
print(f"Point A: {point_a}")
print(f"Point B: {point_b}")
dist = calculate_distance(point_a, point_b)
print(f"Distance between points: {dist:.2f}")

# 8. Lambda functions (anonymous functions)
print("\n8. Lambda Functions:")
square = lambda x: x ** 2
print(f"Square of 7: {square(7)}")

multiply = lambda x, y: x * y
print(f"3 * 4 = {multiply(3, 4)}")

# Using lambda with tuples
points = [(1, 2), (3, 1), (2, 4), (0, 3)]
# Sort points by their y-coordinate (second element of tuple)
sorted_points = sorted(points, key=lambda point: point[1])
print(f"Points sorted by y-coordinate: {sorted_points}")

# 9. Function scope demonstration
global_var = "I'm global"

def scope_demo():
    """Demonstrates local vs global scope."""
    local_var = "I'm local"
    print(f"Inside function - Global: {global_var}")
    print(f"Inside function - Local: {local_var}")

print("\n9. Function Scope:")
scope_demo()
print(f"Outside function - Global: {global_var}")
# print(local_var)  # This would cause an error!

# 10. Practical example: Working with student data
def process_student_data(student_info):
    """
    Process student data stored as tuples.
    student_info: tuple of (name, age, grades_tuple)
    """
    name, age, grades = student_info
    average_grade = sum(grades) / len(grades)
    return {
        'name': name,
        'age': age,
        'grades': grades,
        'average': round(average_grade, 2),
        'status': 'Pass' if average_grade >= 60 else 'Fail'
    }

print("\n10. Practical Example - Student Data:")
student1 = ("John Doe", 20, (85, 92, 78, 88, 91))
student2 = ("Jane Smith", 19, (55, 62, 45, 58, 61))

result1 = process_student_data(student1)
result2 = process_student_data(student2)

print(f"Student 1: {result1}")
print(f"Student 2: {result2}")

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print("""
TUPLES:
- Immutable, ordered collections
- Created with parentheses: (item1, item2, ...)
- Support indexing, slicing, and unpacking
- Good for storing related data that shouldn't change

FUNCTIONS:
- Reusable blocks of code
- Defined with 'def' keyword
- Can have parameters, default values, and return values
- Support *args and **kwargs for flexible arguments
- Have local scope for variables
- Lambda functions for simple, anonymous functions
""")
