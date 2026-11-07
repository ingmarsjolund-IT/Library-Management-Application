
from typing import Optional, List
from infrastructure.db.database import get_connection, init_db
from domain.models import Book


class BookRepo:
    def __init__(self):
        init_db()
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    sql_insert = "INSERT INTO books (book_title, book_author, book_isbn, book_availability, book_genre) VALUES (?, ?, ?, ?, ?)"
    sql_selectall = "SELECT book_title, book_author, book_isbn, book_availability, book_genre FROM books ORDER BY book_isbn"
    sql_selectone = "SELECT book_title, book_author, book_isbn, book_availability, book_genre FROM books WHERE book_isbn = ?"
    sql_update = "UPDATE books SET book_title = ?, book_author = ?, book_availability = ?, book_genre = ? WHERE book_isbn = ?"
    sql_delete = "DELETE FROM books WHERE book_isbn = ?"

    def selectall_books(self) -> List[Book]:
        self.cur.execute(self.sql_selectall)
        rows = self.cur.fetchall()
        return [Book.from_row(row) for row in rows]

    def selectone_book(self, isbn: int) -> Optional[Book]:
        self.cur.execute(self.sql_selectone, (isbn,))
        row = self.cur.fetchone()
        return None if row is None else Book.from_row(row)

    def insert_book(self, book: Book) -> None:
        self.cur.execute(self.sql_insert, (book.book_title, book.book_author, book.book_isbn, book.book_availability, book.book_genre))
        self.conn.commit()

    def update_book(self, book: Book) -> int:
        self.cur.execute(self.sql_update, (book.book_title, book.book_author, book.book_availability, book.book_genre, book.book_isbn))
        self.conn.commit()
        return self.cur.rowcount

    def delete_book(self, isbn: int) -> int:
        self.cur.execute(self.sql_delete, (isbn, ))
        self.conn.commit()
        return self.cur.rowcount

    def close(self) -> None:
        try:
            self.cur.close()
        finally:
            self.conn.close()
