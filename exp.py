import os
import sys


print("Hello World!")
sys.stdout.write("Hello World!")
user_input = input("Enter a directory path (e.g., 'cd C:/Users/amans/Documents/Codium/Z Learning/Python'): ")

# Replace backslashes with forward slashes and ensure changes are assigned back to user_input
user_input = user_input.replace("\\", "/")

# Check if the input starts with 'cd'
if user_input.startswith("cd"):
    parts = user_input.split(" ", 1)  # Split only once to avoid IndexError
    if len(parts) > 1:
        path = parts[1].strip()  # Get the path part and remove any leading/trailing whitespace
        if path == "..":
            os.chdir(os.path.dirname(os.getcwd()))
            print(os.getcwd())
            print("okay if")
        else:
            try:
                os.chdir(path)
                print(os.getcwd())
                print("okay else")
            except FileNotFoundError:
                print(f"The path '{path}' does not exist.")
    else:
        print("No path provided. Usage: cd <path>")

# current_directory = os.getcwd()
# print(current_directory)
# os.chdir("C:/Users/amans/Documents/Codium/Z Learning/Python")
# current_directory = os.getcwd()
# print(current_directory)

