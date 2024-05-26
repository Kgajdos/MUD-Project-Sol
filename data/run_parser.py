import os
from csv_parser import csv_to_python_module

def main():
    # Prompt the user for the CSV file path
    csv_file = input("Enter the path to the CSV file: ")

    # Check if the specified file exists
    if not os.path.isfile(csv_file):
        print("Error: The specified CSV file does not exist.")
        return

    # Prompt the user for the module name
    module_name = input("Enter the name for the Python module: ")

    # Call the csv_to_python_module function with the provided inputs
    csv_to_python_module(csv_file, module_name)

if __name__ == "__main__":
    main()