import feedparser

def fetch_rss_feed(feed_url, limit=5):
    """
    Fetch recent articles metadata from the RSS feed URL.
    Returns list of dicts with keys: title, link, published.
    """
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:limit]:
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', 'N/A')
        })
    return articles


if __name__ == "__main__":
    FEED_URLS = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.ndtv.com/rss/news"
    ]

    for url in FEED_URLS:
        print(f"\nFetching from: {url}")
        articles = fetch_rss_feed(url)

        for idx, article in enumerate(articles, 1):
            print(f"{idx}. {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Published on: {article['published']}\n")
