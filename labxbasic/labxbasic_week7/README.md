
# Introduction to Web Scraping

## Overview
This project introduces web scraping using Python's
requests and BeautifulSoup4 libraries.

## Objective
Extract the book title and chapter titles from:
https://automatetheboringstuff.com/2e/

## Features
- Download HTML content using requests.
- Parse HTML using BeautifulSoup4.
- Extract the book title and chapter titles.
- Handle common HTTP and network errors.
- Save scraped results to a JSON file.

## Installation
Create and activate a virtual environment:

    python3 -m venv ~/testvenv
    source ~/testvenv/bin/activate

Install dependencies:

    python -m pip install requests beautifulsoup4

## How to Run
Run the program from the project directory:

    python main.py

## Ethical Considerations
- Respect the website's robots.txt and Terms of Service.
- Avoid excessive requests.
- Do not collect private or unauthorized information.
- Prefer official APIs when available.
- Use this project for educational purposes.

## Project Structure

    labxbasic_week7/
    ├── src/
    │   ├── __init__.py
    │   └── scraper.py
    ├── data/
    │   └── scraped_output.json
    ├── main.py
    ├── .gitignore
    └── README.md
