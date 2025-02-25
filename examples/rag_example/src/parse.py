import requests
from bs4 import BeautifulSoup
import argparse
import json
import pathlib
from typing import Optional

def fetch_confluence_page(page_url: str) -> str:
    """
    Fetches and parses the content of a Confluence page.

    Args:
        page_url (str): The URL of the Confluence page.

    Returns:
        str: The parsed text content of the page.
    """
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find("body")
        if not body:
            return ""
        text = body.get_text("\n")
        text = " ".join(text.split())  # Normalize whitespace
        print("Website parsed successfully.")
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return ""

def save_text_to_file(url: str) -> None:
    """
    Fetches the content of a Confluence page and saves it to a file.

    Args:
        url (str): The URL of the Confluence page.
    """
    text = fetch_confluence_page(url)
    if not text:
        print("No text to save.")
        return

    current_dir = pathlib.Path().parent.resolve()
    text_dir = current_dir / "temp" / "text"
    text_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    filepath = text_dir / "parsed.txt"

    try:
        with open(filepath, "w", encoding="utf-8") as f:  # Explicit encoding
            f.write(text)
        print(f"Text saved to {filepath}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and chunk a Confluence page.")
    parser.add_argument("url", help="URL of the Confluence page")
    args = parser.parse_args()

    save_text_to_file(args.url)
