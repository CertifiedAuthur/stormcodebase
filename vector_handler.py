import json
import csv
import os

# def jsonl_to_csv(jsonl_file, csv_file, fields):
#     """Convert JSONL to CSV."""
#     with open(jsonl_file, 'r', encoding='utf-8') as infile, open(csv_file, 'w', encoding='utf-8', newline='') as outfile:
#         writer = csv.DictWriter(outfile, fieldnames=fields)
#         writer.writeheader()
#         for line in infile:
#             record = json.loads(line.strip())
#             filtered_record = {field: record.get(field, "") for field in fields}
#             writer.writerow(filtered_record)
#     print(f"Converted {jsonl_file} to {csv_file}")

# def initialize_vectorm(datasets_folder):
#     """Prepare datasets and return the CSV folder path."""
    
#     # Ensure datasets folder exists
#     if not os.path.isdir(datasets_folder):
#         raise ValueError(f"The folder {datasets_folder} does not exist.")
    
#     # Create a CSV subfolder inside datasets folder
#     csv_folder = os.path.join(datasets_folder, "csv")
#     os.makedirs(csv_folder, exist_ok=True)
    
#     fields = ["id", "content", "title", "url", "description"]
    
#     # Convert each JSONL file in datasets_folder to CSV
#     for dataset in os.listdir(datasets_folder):
#         if dataset.endswith(".jsonl"):
#             jsonl_file = os.path.join(datasets_folder, dataset)
#             csv_file = os.path.join(csv_folder, dataset.replace(".jsonl", ".csv"))
#             jsonl_to_csv(jsonl_file, csv_file, fields)
    
#     # Return the folder containing CSV files
#     return csv_folder

def jsonl_to_csv(jsonl_file, csv_file, fields):
    """
    Convert JSONL to CSV with support for nested keys.
    :param jsonl_file: Path to the input JSONL file.
    :param csv_file: Path to the output CSV file.
    :param fields: List of fields to extract, supports dot notation for nested fields.
    """
    def get_nested_value(data, field):
        """
        Extract a nested value from a dictionary using dot notation.
        :param data: The dictionary to extract the value from.
        :param field: The field in dot notation (e.g., 'text.sk').
        :return: The extracted value or an empty string if not found.
        """
        value = data
        for key in field.split('.'):
            if isinstance(value, dict):
                value = value.get(key, "")
            else:
                return ""
        return value

    with open(jsonl_file, 'r', encoding='utf-8') as infile, open(csv_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()

        for line in infile:
            record = json.loads(line.strip())
            filtered_record = {field: get_nested_value(record, field) for field in fields}
            writer.writerow(filtered_record)

    print(f"Converted {jsonl_file} to {csv_file}")

def initialize_vectorm(datasets_folder):
    """
    Prepare datasets and convert JSONL files to CSV.
    :param datasets_folder: Path to the folder containing JSONL files.
    :return: Path to the folder containing CSV files.
    """
    # Ensure datasets folder exists
    if not os.path.isdir(datasets_folder):
        raise ValueError(f"The folder {datasets_folder} does not exist.")

    # Create a CSV subfolder inside datasets folder
    csv_folder = os.path.join(datasets_folder, "csv")
    os.makedirs(csv_folder, exist_ok=True)

    # Define the fields to extract (include nested keys if necessary)
    fields = ["celex_id", "eurovoc_concepts.all_levels", "publication_date", "text.sk"]

    # Convert each JSONL file in datasets_folder to CSV
    for dataset in os.listdir(datasets_folder):
        if dataset.endswith(".jsonl"):
            jsonl_file = os.path.join(datasets_folder, dataset)
            csv_file = os.path.join(csv_folder, dataset.replace(".jsonl", ".csv"))
            jsonl_to_csv(jsonl_file, csv_file, fields)

    # Return the folder containing CSV files
    return csv_folder
