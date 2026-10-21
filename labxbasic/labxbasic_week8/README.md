# Week 19: Automating with CSV and JSON Data
This project focuses on programmatic interaction with two fundamental structured plaintext
data formats: CSV (Comma Separated Values) and JSON (JavaScript Object Notation). You will
learn to read, write, and manipulate data within these files using Python's built-in `csv` and
`json` modules.
## Key Concepts Demonstrated
* **CSV Reading (DictReader)**: Reading CSV files where the first row acts as a header, allowing
data to be accessed as dictionaries (key-value pairs).
* **CSV Writing (DictWriter)**: Writing Python lists of dictionaries back into CSV files, ensuring
proper headers and formatting.
* **CSV Data Processing**: Basic data aggregation (sum, average) and filtering records based
on conditions.
* **JSON Reading (`json.load`)**: Parsing JSON files into Python dictionaries and lists.
* **JSON Writing (`json.dump`)**: Serializing Python objects into JSON files, with options for
pretty-printing for readability.
* **JSON Data Manipulation**: Accessing nested data, updating existing entries, and adding new
data to JSON structures.
* **Modular Design**: Separating CSV and JSON processing logic into distinct modules for
better organization (`csv_handler.py`, `json_handler.py`).

* **Robustness**: Includes basic error handling for file operations and data parsing.
## Setup & How to Run
1. **Clone the repository:**
```bash
git clone
[https://github.com/YOUR_USERNAME/data-processor.git](https://github.com/YOUR_USERNAME/data-pr
ocessor.git)
cd data-processor
```
2. **Install Dependencies:**
Python's `csv` and `json` modules are built-in, so no `pip install` is strictly necessary for these.
However, it's good practice to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate.bat
```
3. **Prepare Input Data Files:**
* Create a folder named `data` in the root of your project: `mkdir data`.
* **`data/input_sales.csv`**: Create a CSV file with sample sales data. The first row should be headers.
* Example content is provided in the `Full Source Code` section above.
* **`data/input_inventory.json`**: Create a JSON file with sample product inventory data.
* Example content is provided in the `Full Source Code` section above.
4. **Run the script:**
```bash
python main.py
```
The script will:
* Read `data/input_sales.csv`.
* Process the sales data, filtering records where 'Amount' is >= $100 and calculating totals/averages.
* Write the filtered sales data (with a summary row) to `data/output_filtered_sales.csv`.
* Read `data/input_inventory.json`.
* Update stock levels for `PROD001` and `PROD003`.
* Add a new product (`PROD004`).
* Write the updated inventory data to `data/output_updated_inventory.json`.
## Project Structure

data-processor/
├── src/
│ ├── init.py # Python package marker
│ ├── csv_handler.py # Encapsulates CSV operations

│ ├── json_handler.py # Encapsulates JSON operations
│ └── utils.py # Logging and directory creation
├── data/
│ ├── input_sales.csv # Sample input CSV (YOU CREATE)
│ ├── output_filtered_sales.csv # Output: Filtered CSV with summary
│ ├── input_inventory.json # Sample input JSON (YOU CREATE)
│ └── output_updated_inventory.json # Output: Updated JSON
├── main.py # Application entry point
├── .gitignore # Files/folders to ignore in Git
└── README.md # This project overview

## Debugging CSV and JSON Automation
* **`FileNotFoundError`**: Ensure your input files (`input_sales.csv`, `input_inventory.json`) are
correctly placed in the `data` directory.
* **`KeyError` in CSV Processing**:
* This usually means the header names in your `input_sales.csv` do not exactly match the
keys you're trying to access (e.g., `'Amount'`, `'Price'`). Check for typos or leading/trailing
spaces in headers.
* Ensure `fieldnames` passed to `DictWriter` match the keys in your dictionaries.
* **`json.JSONDecodeError`**:
* This indicates invalid JSON syntax in your `input_inventory.json`. Use an online JSON
validator or a good text editor (like VS Code with JSON formatting) to check for missing
commas, unquoted keys/values, or incorrect brackets/braces.
* Ensure the file is saved with UTF-8 encoding.
* **`ValueError` (e.g., `could not convert string to float`)**:
* This happens when numeric fields in your CSV (`Amount`, `Price`) contain non-numeric
characters (e.g., currency symbols like '$', commas, or empty strings). You'll need to clean these
strings before converting to `float()`. The current `csv_handler.py` includes basic `try-except`
blocks for this.
* **Data Not Updating in JSON**:
* Verify that the `product_id` you're trying to update in `json_proc.update_inventory()`
actually exists in your `input_inventory.json`.
* Ensure the structure of `inventory_data` is a list of dictionaries as expected by the
`update_inventory` function.
* **Encoding Issues**: If you see strange characters in your output files, ensure both reading
and writing operations use `encoding='utf-8'`.

## Extension Ideas (Future Work)
* **CSV-to-JSON / JSON-to-CSV Converter**: Build a dedicated script or function to convert
data between these two formats, handling nested JSON to flat CSV and vice-versa.
* **Data Validation**: Implement more robust validation logic for input data (e.g., ensuring
numeric fields are indeed numbers, checking for required fields).
* **Large File Processing**: For very large CSV/JSON files, explore techniques like reading in
chunks or using libraries optimized for large data (e.g., `pandas` for tabular data, or `ijson` for
streaming JSON).
* **Integration with Web APIs**: Many web APIs communicate using JSON. Practice sending
requests to and parsing responses from public APIs.
* **Database Interaction**: Use CSV/JSON files as an intermediary for importing data into or
exporting data from simple databases (e.g., SQLite).
* **Configuration Management**: Use JSON files to store more complex application settings
and load them dynamically at runtime.
* **Automated Reporting**: Generate summary reports (e.g., HTML or plain text) based on
processed CSV/JSON data.
---
แหลง่ ทม
ี่
า
1. https://github.com/MarshallDoyle/Patent
2. https://github.com/MikeyBeez/RAGAgent
3. https://automatetheboringstuff.com/2e/chapter16/