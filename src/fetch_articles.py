import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article

# Directory to save articles
OUTPUT_DIR = "data/articles"

def fetch_article(url, output_dir=OUTPUT_DIR):
    """Fetches article content from a URL and saves it as a text file."""
    try:
        # Use newspaper3k for extraction
        article = Article(url)
        article.download()
        article.parse()

        # Get article title for file naming
        title = article.title.replace(" ", "_").replace("/", "_")
        filename = f"{title[:50]}.txt"  # Limit to 50 characters

        # Save the content
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Title: {article.title}\n\n")
            f.write(article.text)

        print(f"Saved article: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return None

if __name__ == "__main__":
    # Example URLs
    urls = [
        "https://www.pff.com/news/fantasy-football-season-2024-in-review-what-nathan-jahnke-got-right-and-wrong",
        "https://bellyupsports.com/2025/01/fantasy-football-season-review/",
        "https://underdognetwork.com/football/best-ball-research/the-2024-fantasy-football-season-recap",
        "https://sports.yahoo.com/these-were-the-keys-to-victory-for-the-2024-fantasy-football-season-155326629.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAANSKzDlqVlByYkVTrT-Hzpp-jbWfMI2GIPMXcBL6umGSVQd4x5EgQWnTR0i2eFssZwrqQLhx5bzJkHFGgGOT2CKuY35ZLD7po6MoTkMtggNzcT2oL7al-Dt7WoDS46LR57RP-n8QscCSY-q575AdFFFn8vMxV742HG6kkB_bJdmX",
        "https://sports.yahoo.com/fantasy-football-fact-or-fluke-how-to-make-memories-from-the-2024-season-work-for-you-in-2025-154207119.html"
    ]
    for url in urls:
        fetch_article(url)
