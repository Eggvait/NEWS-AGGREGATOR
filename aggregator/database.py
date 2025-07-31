import sqlite3

def create_connection(db_file="news.db"):
    """
    Create and return a connection to SQLite database file.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    return conn

def create_articles_table(conn):
    """
    Create articles table if not exists.
    """
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        authors TEXT,
        publish_date TEXT,
        content TEXT,
        source TEXT,
        fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Articles table created or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating articles table: {e}")

def insert_article(conn, article):
    """
    Insert an article dict into articles table.
    """
    insert_sql = '''
    INSERT OR IGNORE INTO articles (url, title, authors, publish_date, content, source)
    VALUES (?, ?, ?, ?, ?, ?);
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(insert_sql, (
            article['url'],
            article['title'],
            article['authors'],
            article['publish_date'],
            article['content'],
            article['source']
        ))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Inserted article: {article['title']}")
        else:
            print(f"Article already exists, skipping: {article['title']}")
    except sqlite3.Error as e:
        print(f"Error inserting article: {e}")
