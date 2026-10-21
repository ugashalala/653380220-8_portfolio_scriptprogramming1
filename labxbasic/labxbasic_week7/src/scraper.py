
import requests
from bs4 import BeautifulSoup


class SimpleWebScraper:
    """A class to perform basic web scraping."""

    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        """Download HTML content from the target website."""
        print(f"Downloading content from: {self.target_url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; EducationalScraper/1.0)"
        }

        try:
            response = requests.get(
                self.target_url,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            print("Successfully downloaded content.")
            return response.text

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout:
            print("The request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")

        return None

    def scrape_main_titles(self):
        """Extract the book title and chapter titles."""
        html_content = self._get_html_content()

        if html_content is None:
            return None

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the book title
        page_header = soup.find("div", class_="page-header")
        book_title_tag = (
            page_header.find("h1") if page_header else soup.find("h1")
        )

        if book_title_tag:
            book_title = book_title_tag.get_text(" ", strip=True)
        elif soup.title:
            book_title = soup.title.get_text(" ", strip=True)
        else:
            book_title = "Book Title Not Found"

        # Extract chapter titles from the table of contents
        chapter_titles = []
        toctree_wrapper = soup.find("div", class_="toctree-wrapper")

        if toctree_wrapper:
            chapter_links = toctree_wrapper.select(
                "li.toctree-l1 a.reference.internal"
            )

            for link in chapter_links:
                title = link.get_text(" ", strip=True)
                if title and title not in chapter_titles:
                    chapter_titles.append(title)

        # Fallback: look for chapter links if the expected structure is absent
        if not chapter_titles:
            for link in soup.find_all("a", href=True):
                href = link.get("href", "").lower()
                title = link.get_text(" ", strip=True)

                if "chapter" in href and title and title not in chapter_titles:
                    chapter_titles.append(title)

        return {
            "book_title": book_title,
            "chapter_titles": chapter_titles
        }
