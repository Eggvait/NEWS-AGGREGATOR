from aggregator.fetcher import fetch_rss_feed
from aggregator.parser import extract_article_content
from aggregator.database import create_connection, create_articles_table, insert_article

FEED_URLS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.ndtv.com/rss/news"
]

def main():
    # Step 1: Connect to DB and create table
    conn = create_connection()
    if conn is None:
        print("Failed to connect to the database. Exiting.")
        return

    create_articles_table(conn)

    # Step 2: For each RSS feed
    for feed_url in FEED_URLS:
        print(f"\nFetching articles from: {feed_url}")
        try:
            metadata_list = fetch_rss_feed(feed_url, limit=3)  # Fetch top 3 for demo
        except Exception as e:
            print(f"Failed to fetch feed {feed_url}: {e}")
            continue

        # Step 3: Parse each article and save to DB
        for meta in metadata_list:
            print(f"\nProcessing article: {meta['title']}")
            try:
                full_article = extract_article_content(meta['link'])
                article_data = {
                    'url': meta['link'],
                    'title': full_article['title'] or meta['title'],
                    'authors': ', '.join(full_article['authors']) if full_article['authors'] else 'Unknown',
                    'publish_date': str(full_article['publish_date']) if full_article['publish_date'] else meta['published'],
                    'content': full_article['text'],
                    'source': feed_url
                }
                insert_article(conn, article_data)
            except Exception as e:
                print(f"Error processing article {meta['link']}: {e}")

    conn.close()
    print("\nAll done! Database connection closed.")

if __name__ == "__main__":
    main()
