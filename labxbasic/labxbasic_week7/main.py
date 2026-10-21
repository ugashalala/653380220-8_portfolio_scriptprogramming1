
import json
from pathlib import Path

from src.scraper import SimpleWebScraper


def main():
    """Main entry point of the application."""
    target_url = "https://automatetheboringstuff.com/2e/"

    scraper = SimpleWebScraper(target_url)
    scraped_data = scraper.scrape_main_titles()

    if scraped_data is None:
        print("Failed to scrape data.")
        return

    print("\n--- Scraped Data ---")
    print(f"Book Title: {scraped_data['book_title']}")
    print("\nChapter Titles:")

    if scraped_data["chapter_titles"]:
        for i, title in enumerate(
            scraped_data["chapter_titles"], start=1
        ):
            print(f"{i}. {title}")
    else:
        print("No chapter titles found.")
        print("The website's HTML structure may have changed.")

    # Save the results as JSON
    output_path = Path("data/scraped_output.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(scraped_data, file, ensure_ascii=False, indent=4)

    print(f"\nResults saved to: {output_path}")
    print("--------------------")


if __name__ == "__main__":
    main()
