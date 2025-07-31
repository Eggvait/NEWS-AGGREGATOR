from aggregator.fetcher import fetch_rss_feed
from aggregator.parser import extract_article_content

FEED_URLS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.ndtv.com/rss/news"
]

def main():
    all_articles = []

    for feed_url in FEED_URLS:
        print(f"\n--- Fetching articles from: {feed_url} ---")
        articles_metadata = fetch_rss_feed(feed_url, limit=3)  # limit 3 for demo

        for article_meta in articles_metadata:
            print(f"\nFetching full content for article: {article_meta['title']}")
            try:
                article_full = extract_article_content(article_meta['link'])
                print(f"Title: {article_full['title']}")
                print(f"Authors: {article_full['authors']}")
                print(f"Publish Date: {article_full['publish_date']}")
                print(f"Content snippet: {article_full['text'][:300]}...\n")
                all_articles.append(article_full)
            except Exception as e:
                print(f"Failed to extract article content: {e}")

    print(f"\nTotal articles fetched and parsed: {len(all_articles)}")

if __name__ == "__main__":
    main()
