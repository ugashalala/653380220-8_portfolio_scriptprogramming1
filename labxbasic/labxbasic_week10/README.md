
# Week 10: Automating Spreadsheets (Excel & Google Sheets)

This project demonstrates how to automate Microsoft Excel
.xlsx files using Python and the openpyxl library.

## Key Features

- Load existing Excel workbooks.
- Read and write cell values.
- Calculate total prices for each product.
- Calculate the grand total of all sales.
- Format cells with fonts, colors, borders, and number formats.
- Automatically adjust column widths.

## Requirements

- Python
- openpyxl

## Installation

Install the required library:

```bash
pip install openpyxl
```

## Input Data

Create a folder named data and add an Excel file named
input_sales.xlsx.

The first sheet should contain these columns:

- Product Name
- Quantity
- Unit Price

Data should begin on row 2.

## How to Run

Run the following command from the project root:

```bash
python main.py
```

## Output

The program generates:

data/output_sales_report.xlsx

The output contains the original sales data, total price
for each product, grand total, and basic formatting.
