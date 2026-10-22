
# Week 20: Agentic Data Processing (Advanced CSV & JSON Workflows)

This project demonstrates an "Agentic Data Processor" that orchestrates complex data
manipulation workflows for CSV and JSON files based on a declarative JSON configuration. It
showcases advanced data transformation, cross-format conversion, and robust state
management within the agent.

## Key Concepts Demonstrated

* **Agentic Workflow Orchestration**: The `DataAgent` reads a pipeline defined in
  `configs/data_pipeline_config.json` and executes tasks sequentially, managing the flow of data
  between steps.
* **Internal Data Store**: The agent maintains an in-memory `data_store` (`self.data_store`) to
  pass intermediate processed data (as Python lists of dicts or nested dicts/lists) between tasks
  using user-defined keys.
* **Advanced CSV Processing**:
* Loading CSV data as a list of dictionaries (`DictReader`).
* **Aggregation**: Grouping data by a field (e.g., `Customer`) and performing calculations
  (e.g., `sum` of `Amount`).
* Saving processed data back to CSV (`DictWriter`).
* **Advanced JSON Processing**:
* Loading and saving JSON data.
* **Dynamic Updates**: Applying multiple updates to nested JSON structures using a
  dot-notation path, including `set` operations and `Notes`.
* **Querying Data**: Extracting specific values from nested JSON using a path.
* **Cross-Format Conversion**:
* Converting a list of dictionaries (from CSV) into a JSON-compatible Python object.
* (Conceptual) Converting JSON back to CSV, handling simple nested structures.
* **Modularity**: Code is organized into `csv_tasks.py`, `json_tasks.py`, `conversion_tasks.py`,
  `config_parser.py`, and `utils.py` for clarity and reusability.
* **Robustness**: Includes comprehensive error handling and an audit logging mechanism to
  track every step of the agent's execution.

## Setup & How to Run

1. **Clone the repository:**

```bash
git clone
[https://github.com/YOUR_USERNAME/agentic-data-processor.git](https://github.com/YOUR_USERNAME
/agentic-data-processor.git)
cd agentic-data-processor
```

2. **Install Dependencies:**

Python's `csv` and `json` modules are built-in.
It's recommended to use a virtual environment:

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

4. **Review `configs/data_pipeline_config.json`:**

* This file defines the entire data processing workflow.
* **Crucially**, ensure that the `file_path` values in the JSON config accurately point to your created
  input files, relative to the project root.
* Feel free to modify the `tasks` to experiment with different aggregations, filters, or JSON
  transformations.

5. **Run the script:**

```bash
python main.py
```

The script will execute the pipeline defined in `data_pipeline_config.json`:

* Load `input_sales.csv`.
* Aggregate sales by customer and save to `data/processed_sales_by_customer.csv`.
* Convert the raw sales data to JSON and save to `data/sales_data.json`.
* Load `input_inventory.json`.
* Apply various updates to the inventory data (stock levels, add new product).
* Query a specific detail from the updated inventory.
* Save the updated inventory data to `data/updated_inventory.json`.
* Generate a detailed `audit_report_*.json` in the `reports/` directory.

## Project Structure

agentic-data-processor/
├── src/
│ ├── init.py # Python package marker
│ ├── data_agent.py # Core agent logic: orchestrates tasks and manages data state
│ ├── csv_tasks.py # Functions for loading, saving, aggregating, filtering CSVs
│ ├── json_tasks.py # Functions for loading, saving, updating, querying JSON
│ ├── conversion_tasks.py # Functions for converting CSV <-> JSON
│ ├── config_parser.py # Loads and validates the JSON pipeline configuration

│ └── utils.py # Logging, directory creation, audit logging utilities
├── configs/
│ └── data_pipeline_config.json # The declarative JSON configuration for the data pipeline
├── data/
│ ├── input_sales.csv # Sample input CSV (YOU CREATE)
│ ├── input_inventory.json # Sample input JSON (YOU CREATE)
│ ├── processed_sales_by_customer.csv # Output: Aggregated sales CSV
│ ├── sales_data.json # Output: Sales data converted to JSON
│ └── updated_inventory.json # Output: Modified inventory JSON
├── main.py # Application entry point
├── .gitignore # Files/folders to ignore in Git
└── README.md # This project overview

## Debugging Advanced Data Workflows

* **`FileNotFoundError`**:
* Ensure `input_sales.csv` and `input_inventory.json` are correctly placed in the `data`
  directory.
* Check that `file_path` entries in `data_pipeline_config.json` correctly point to your files
  (relative to the project root).
* **`KeyError` in CSV/JSON Processing**:
* Verify that column names in your CSV headers and keys in your JSON exactly match what
  the tasks expect (e.g., `Customer`, `Amount` in CSV; `id`, `stock` in JSON).
* For JSON `path` updates/queries, ensure the dot-notation path (`key1.key2.index`)
  correctly reflects your JSON structure.
* **Invalid JSON/CSV Format**:
* Use online validators or good IDE features to check your `input_inventory.json` and
  `data_pipeline_config.json` for syntax errors (missing commas, incorrect brackets, etc.).
* For CSVs, ensure consistent delimiters and proper quoting if fields contain commas.
* **Data Not Changing/Processing Incorrectly**:
* **Check `input_data_key` and `output_data_key`**: Ensure that the `output_data_key` of a
  preceding task matches the `input_data_key` of a subsequent task if you intend to chain them.
* **Review Task Parameters**: Double-check parameters like `group_by_field`,
  `aggregate_field`, `operator`, `path`, `value` in `data_pipeline_config.json` for correctness.
* **Log Output**: Pay close attention to the console logs and the generated
  `audit_report_*.json` in the `reports/` directory. They provide detailed messages about task
  status, errors, and intermediate data.
* **Type Conversion Issues**: The `csv_to_json` function attempts basic type conversion (int,

float, boolean, null). If your data is more complex (e.g., dates), you'll need to add specific
handling in `conversion_tasks.py`.

## Extension Ideas (Future Work)

* **More Complex CSV Joins/Merges**: Implement functions for SQL-like `INNER JOIN`, `LEFT JOIN` on multiple CSV files. For very large datasets, consider integrating with `pandas`.
* **Advanced JSON Transformations (Jinja2/Jmespath)**: Allow more complex JSON
  transformations using template engines (like Jinja2 for generating JSON) or query languages
  like JMESPath directly within the config.
* **Data Validation with Schemas**: Integrate `jsonschema` library to validate input JSON or
  CSV data against a predefined schema. This ensures data quality before processing.
* **Error Handling Strategies**: Implement more sophisticated error handling, such as retries,
  fallback operations, or custom error reporting mechanisms (e.g., sending email notifications on
  failure).
* **Conditional Task Execution**: Add logic to the `DataAgent` to execute tasks conditionally
  based on the results of previous tasks or external factors.
* **Dynamic Source/Destination**: Allow `file_path` to be dynamic, perhaps constructed from
  global data or previous task outputs (e.g., `output_path_prefix + date + .csv`).
* **External Data Sources**: Extend `load_csv`/`load_json` tasks to fetch data from URLs (web
  APIs), databases, or cloud storage.
* **Web Interface**: Build a simple Flask/Streamlit web application that allows users to upload
  configuration files and view processing results/audit logs.

---

แหลง่ ทม
ี่
า

1. https://github.com/kykoo/gcam
2. https://github.com/MarshallDoyle/Patent
3. https://github.com/MikeyBeez/RAGAgent
