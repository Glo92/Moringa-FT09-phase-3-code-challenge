import sqlite3

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category


    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")
        
        
    def _create_magazine(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)',
                        (self._name, self._category))
        connection.commit()

        magazine_id = cursor.lastrowid
        connection.close()
        return magazine_id

    def _get_magazine_from_db(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name, category FROM magazines WHERE id = ?', (self._id,))
        name, category = cursor.fetchone()
        connection.close()
        return name, category


    def articles(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def contributors(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        connection.close()
        return contributors

    def article_titles(self):
        articles = self.articles()
        if articles:
            return [article[1] for article in articles]
        return None

    def contributing_authors(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) FROM authors JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        connection.close()
        if authors:
            return [(author[0]) for author in authors]
        return None
