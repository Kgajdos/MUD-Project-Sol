import csv
import os

def csv_to_python_module(csv_file, module_name):
    # Check if the Python module file already exists
    module_file_path = f'{module_name}.py'
    file_exists = os.path.isfile(module_file_path)

    # Open the CSV file for reading
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)

        # Open the Python module file for appending
        with open(module_file_path, 'a') as module_file:
            # If the file doesn't exist yet, add module header
            if not file_exists:
                module_file.write('# This module was auto-generated from a CSV file\n\n')

            # Iterate over each row in the CSV file
            for row in reader:
                # Check if the entry already exists in the Python module file
                if not entry_exists(module_file_path, row["prototype_key"]):
                    # Write each row as a dictionary to the Python module
                    module_file.write(f'{row["prototype_key"]} = {{\n')
                    for key, value in row.items():
                        if key != "prototype_key":
                            if isinstance(value, int):
                                module_file.write(f'    "{key}": {value},\n')
                            else:
                                if value:
                                    module_file.write(f'    "{key}": "{value}",\n')
                                else:
                                    module_file.write(f'    "{key}": None,\n')
                    # Additional formatting for the "attrs" key
                    if "desc" in row and "quality" in row:
                        module_file.write(f'    "attrs": [("desc", "{row["desc"]}"), ("quality", "{row["quality"]}")],\n')
                    module_file.write('}\n\n')


def entry_exists(file_path, entry_key):
    # Check if the entry key already exists in the Python module file
    with open(file_path, 'r') as module_file:
        for line in module_file:
            if entry_key in line:
                return True
    return False

