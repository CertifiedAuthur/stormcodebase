import json
from datasets import load_dataset

# Load processed EuroVoc data
processed_eurlex_path = "processed_eurlex_data.json"
print(f"[INFO] Loading processed EuroVoc data from: {processed_eurlex_path}")
try:
    with open(processed_eurlex_path, "r", encoding="utf-8") as file:
        processed_eurlex_data = json.load(file)
    print("[INFO] Processed EuroVoc data loaded successfully.")
except FileNotFoundError:
    print(f"[ERROR] File not found: {processed_eurlex_path}")
    exit(1)

# Create a mapping from document_id to labels and descriptions
eurovoc_map = {
    entry["document_id"]: entry["labels"] for entry in processed_eurlex_data
}

# Load the Multi-EURLEX dataset
print("[INFO] Loading the Multi-EURLEX dataset (English version)...")
dataset = load_dataset("nlpaueb/multi_eurlex", "en", trust_remote_code=True)

# Process the dataset and create the desired output format
output_data = []
for sample in dataset["train"]:  # Replace "train" with the desired split (train/test/validation)
    celex_id = sample["celex_id"]
    text = {"en": sample["text"]}  # Extract text (assuming 'text' contains the English version)

    # Retrieve labels from the processed EuroVoc data
    labels = eurovoc_map.get(celex_id, [])
    
    # Combine into a structured entry
    entry = {
        "celex_id": celex_id,
        "text": text,
        "labels": labels
    }
    output_data.append(entry)

# Save the structured data to a JSON file
output_file = "multi_eurlex_structured.json"
with open(output_file, mode="w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, indent=4, ensure_ascii=False)

print(f"[INFO] Structured dataset saved to: {output_file}")




import json
import csv

# Load JSON data
input_file = "multi_eurlex_structured.json"
output_file = "multi_eurlex_structured.csv"

# Read the JSON file
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare the CSV output
csv_data = []
for idx, item in enumerate(data, start=1):
    celex_id = item.get("celex_id", f"unknown-{idx}")
    content = item.get("text", {}).get("en", "No content available")
    title = f"Document {idx}"
    url = f"docu-{celex_id}"
    description = "A document related to: " + ", ".join(
        label.get("eurovoc_desc", "general topic") for label in item.get("labels", [])
    )
    csv_data.append([content, title, url, description])

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["content", "title", "url", "description"])  # Header
    writer.writerows(csv_data)

print(f"CSV file saved as {output_file}")