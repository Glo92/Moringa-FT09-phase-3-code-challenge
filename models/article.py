import sqlite3

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self.title = title
        self.content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be a string between 5 and 50 characters.")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._content = value
        else:
            raise ValueError("Content must be a non-empty string.")

    @property
    def author(self):
        return (self._author_id)

    @property
    def magazine(self):
        return (self._magazine_id)

    def _create_article(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (self._title, self._content, self._author_id, self._magazine_id))
        connection.commit()
        article_id = cursor.lastrowid
        connection.close()
        return article_id

    def _get_article_from_db(self):
        connection = sqlite3.connect('magazine.db')
        cursor = connection.cursor()
        cursor.execute('SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?', (self._id,))
        title, content, author_id, magazine_id = cursor.fetchone()
        connection.close()
        return title, content, author_id, magazine_id
