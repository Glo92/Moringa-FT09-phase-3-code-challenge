from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    while True:
        author_name = input("Enter author's name: ")
        if len(author_name) > 0:
            break
        print("Author name cannot be empty. Please try again.")

    while True:
        magazine_name = input("Enter magazine name: ")
        if len(magazine_name) > 0 and len(magazine_name) <= 16:
            break
        print("Magazine name must be between 1 and 16 characters. Please try again.")

    while True:
        magazine_category = input("Enter magazine category: ")
        if len(magazine_category) > 0:
            break
        print("Magazine category cannot be empty. Please try again.")

    while True:
        article_title = input("Enter article title: ")
        if len(article_title) > 4 and len(article_title) <= 50:
            break
        print("Article title must be between 5 and 50 characters. Please try again.")

    while True:
        article_content = input("Enter article content: ")
        if len(article_content) > 0:
            break
        print("Article content cannot be empty. Please try again.")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Fetch the inserted records
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine[0], magazine[1], magazine[2]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author[0], author[1]))

    print("\nArticles:")
    for article in articles:
        print(Article(article[0], article[1], article[2], article[3], article[4]))

if __name__ == "__main__":
    main()
