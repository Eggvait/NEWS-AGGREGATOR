import requests
import newspaper
from bs4 import BeautifulSoup

def extract_authors_from_html(html):
    """
    Try to extract author(s) from HTML meta tags as fallback.
    Returns list of authors or empty list.
    """
    soup = BeautifulSoup(html, 'html.parser')
    authors = []

    # Common meta tags for author
    meta_author = soup.find('meta', attrs={'name': 'author'})
    if meta_author and meta_author.get('content'):
        authors.append(meta_author['content'].strip())

    # Facebook Open Graph property for author
    og_author = soup.find('meta', attrs={'property': 'article:author'})
    if og_author and og_author.get('content'):
        authors.append(og_author['content'].strip())

    # Twitter creator tag
    twitter_creator = soup.find('meta', attrs={'name': 'twitter:creator'})
    if twitter_creator and twitter_creator.get('content'):
        authors.append(twitter_creator['content'].strip())

    # Remove duplicates and empty strings
    authors = list(set([a for a in authors if a]))

    return authors

def extract_article_content(url):
    """
    Extract full article data with enhanced author extraction.

    Args:
        url (str): Article URL.

    Returns:
        dict: title, authors (list), publish_date, text
    """
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to retrieve article page: {e}")

    article = newspaper.Article(url)
    article.set_html(response.text)

    try:
        article.parse()
    except Exception as e:
        raise Exception(f"Failed to parse article content: {e}")

    authors = article.authors

    # Fallback if no authors found by newspaper3k
    if not authors:
        authors = extract_authors_from_html(response.text)

    if not authors:
        authors = ["Unknown"]

    return {
        'title': article.title,
        'authors': authors,
        'publish_date': article.publish_date,
        'text': article.text
    }

if __name__ == "__main__":
    test_urls = [
        "https://www.ndtv.com/india-news/modi-launches-highway-projects-worth-rs-1-lakh-crore-in-maharashtra-4253000",
        "https://www.thehindu.com/news/national/tamil-nadu/tamil-nadu-to-get-50-electric-buses-on-lease/article67287623.ece",
        "https://timesofindia.indiatimes.com/india/india-faces-severe-power-crisis-in-summer-power-minister/articleshow/103456789.cms"
    ]

    for url in test_urls:
        print(f"\nExtracting article from: {url}")
        try:
            article_data = extract_article_content(url)
            print("Title:", article_data['title'])
            print("Authors:", article_data['authors'])
            print("Publish Date:", article_data['publish_date'])
            print("Snippet:\n", article_data['text'][:500], "...\n")
        except Exception as e:
            print(f"Error: {e}\nSkipping this article.\n")
