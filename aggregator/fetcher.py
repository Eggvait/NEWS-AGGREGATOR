import feedparser

def fetch_rss_feed(feed_url, limit=5):
    """
    Fetches and parses RSS feed from the URL.

    Args:
        feed_url (str): URL to the RSS feed.
        limit (int): Number of articles to fetch for testing.

    Returns:
        list of dict: Each dict has 'title', 'link', 'published' keys.
    """
    feed = feedparser.parse(feed_url)
    articles = []

    # Iterate over entries, limit for demo
    for entry in feed.entries[:limit]:
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', 'N/A')
        })
    return articles


if __name__ == "__main__":
    # Example test feeds
    FEED_URLS = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.ndtv.com/rss/news"
    ]

    for url in FEED_URLS:
        print(f"Fetching from: {url}")
        articles = fetch_rss_feed(url)

        for idx, article in enumerate(articles, 1):
            print(f"{idx}. {article['title']}")
            print(f"    Link: {article['link']}")
            print(f"    Published on: {article['published']}\n")
