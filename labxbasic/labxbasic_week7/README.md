# Week 13: Introduction to Web Scraping
This project introduces the fundamentals of web scraping using Python&#39;s `requests` and
`BeautifulSoup4` libraries. It demonstrates how to download HTML content from a website and
extract specific information based on HTML structure.
**Important Note on Ethics and Legality:**
Always be mindful of the website&#39;s `robots.txt` file (e.g., `https://example.com/robots.txt`) and their
Terms of Service. Respect rate limits and avoid overwhelming servers. This project is for
educational purposes only and should not be used for malicious or unauthorized data collection.
## Implemented Features
* **HTML Download**: Uses the `requests` library to fetch web page content.
* **HTML Parsing**: Leverages `BeautifulSoup4` to parse the downloaded HTML.
* **Data Extraction**: Extracts the main book title and a list of chapter titles from the &quot;Automate
the Boring Stuff with Python&quot; website.
* **Error Handling**: Basic error handling for network issues and HTTP responses.
## How to Run
1. **Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/web-scraping-
intro.git](https://github.com/YOUR_USERNAME/web-scraping-intro.git)
cd web-scraping-intro
```
2. **Install Dependencies:**
You&#39;ll need `requests` and `beautifulsoup4`. It&#39;s recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install requests beautifulsoup4
```
3. **Run the scraper:**
```bash
python main.py
```
The script will print the scraped book title and chapter titles to the console.
## Project Structure

web-scraping-intro/
├── src/
│ ├── init.py # Makes &#39;src&#39; a Python package
│ └── scraper.py # Contains the core web scraping logic
├── main.py # Application entry point
├── .gitignore # Files/folders to ignore in Git
└── README.md # This project overview

## Debugging Web Scraping
* **Inspect HTML:** Use your browser&#39;s developer tools (F12 or Ctrl+Shift+I) to inspect the
HTML structure of the page you&#39;re scraping. This is crucial for identifying the correct tags,
classes, and IDs to target with `BeautifulSoup`.
* **Print `response.status_code`:** Check if your request was successful (200 OK) or if there
was an issue (e.g., 403 Forbidden, 404 Not Found).
* **Print `response.text`:** Sometimes it&#39;s useful to print the raw HTML content to see if you&#39;re
getting what you expect, especially if parsing fails.
* **Check for `None`:** When using `find()` or `select()`, always check if the returned element is
`None` before trying to access its attributes or text, to prevent `AttributeError`s.
* **User-Agent:** Some websites block requests without a `User-Agent` header. Adding
`headers = {&#39;User-Agent&#39;: &#39;Your Custom User Agent&#39;}` can help.
* **Rate Limiting:** If you make too many requests too quickly, a site might temporarily block
you. Add `time.sleep()` between requests (import `time`).
## Extension Ideas
* **Save Data to File**: Modify `scraper.py` to save the extracted data to a CSV or JSON file
(`data/scraped_output.json`).
* **Scrape Multiple Pages**: Extend the scraper to navigate through multiple pages (e.g.,
paginate through a blog archive).
* **Extract More Data**: Beyond titles, extract links, dates, authors, or article content.
* **Handle Dynamic Content (Selenium)**: For websites that load content dynamically with
JavaScript, research and experiment with `Selenium` to control a browser. (Requires browser
driver setup).
* **Error Reporting**: Implement more sophisticated error logging to a file.
* **Parameterize URL/Selectors**: Allow the user to input the URL and potentially even CSS
selectors.
## License
This project is open source. (You might add a specific license here later, e.g., MIT)

Source:
● Automate the Boring Stuff with Python, 2nd Edition - Chapter 12: Web Scraping:
https://automatetheboringstuff.com/2e/chapter12/
แหล่งที่มา
1. https://devpress.csdn.net/python/63051124c67703293080ea76.html
2. https://github.com/BobTheSnob1/dominion_staff_timeline
3. https://github.com/MikeyBeez/RAGAgent
4. https://automatetheboringstuff.com/2e/chapter12/