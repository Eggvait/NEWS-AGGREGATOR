import requests
import newspaper
from bs4 import BeautifulSoup

def extract_authors_from_html(html):
    """
    Fallback to extract authors from common meta tags in HTML.
    Returns a list of authors or empty list.
    """
    soup = BeautifulSoup(html, 'html.parser')
    authors = []

    meta_author = soup.find('meta', attrs={'name': 'author'})
    if meta_author and meta_author.get('content'):
        authors.append(meta_author['content'].strip())

    og_author = soup.find('meta', attrs={'property': 'article:author'})
    if og_author and og_author.get('content'):
        authors.append(og_author['content'].strip())

    twitter_creator = soup.find('meta', attrs={'name': 'twitter:creator'})
    if twitter_creator and twitter_creator.get('content'):
        authors.append(twitter_creator['content'].strip())

    # Remove duplicates and empty strings
    return list(set([a for a in authors if a]))

def extract_article_content(url):
    """
    Fetch and parse full article content including enhanced author extraction.
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
    sample_url = "https://www.ndtv.com/india-news/modi-launches-highway-projects-worth-rs-1-lakh-crore-in-maharashtra-4253000"
    print(f"Extracting article from: {sample_url}")

    try:
        article_data = extract_article_content(sample_url)
        print("Title:", article_data['title'])
        print("Authors:", article_data['authors'])
        print("Publish Date:", article_data['publish_date'])
        print("\nSnippet:\n", article_data['text'][:500], "...\n")
    except Exception as e:
        print(f"Error: {e}")
