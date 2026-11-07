
from typing import List
from domain.models import Book, ViewBook
from infrastructure.db.book_repo import BookRepo


class ManageBook:
    @staticmethod
    def _validate(vb: ViewBook) -> List[str]:
        errs = []
        if not vb.title.strip():
            errs.append("Book title is required.")
        if not vb.author.strip():
            errs.append("Book author is required.")
        if not vb.isbn.strip():
            errs.append("Book ISBN is required.")
        if vb.isbn and not vb.isbn.isdigit():
            errs.append("ISBN must be a number.")
        if not vb.genre.strip():
            errs.append("Book genre is required.")
        if not vb.availability.strip():
            errs.append("Book availability is required.")
        return errs

    @staticmethod
    def CreateBook(vb: ViewBook) -> List[str]:
        errs = ManageBook._validate(vb)
        if errs:
            return errs
        book = Book(
            book_title=vb.title.strip(),
            book_author=vb.author.strip(),
            book_isbn=int(vb.isbn),
            book_genre=vb.genre.strip(),
            book_availability=vb.availability.strip(),
        )
        repo = BookRepo()
        try:
            repo.insert_book(book)
        finally:
            repo.close()
        return []

    @staticmethod
    def GetAllBooks() -> List[ViewBook]:
        repo = BookRepo()
        try:
            books = repo.selectall_books()
        finally:
            repo.close()
        return [
            ViewBook(
                title=b.book_title,
                author=b.book_author,
                isbn=str(b.book_isbn),
                genre=b.book_genre,
                availability=b.book_availability,
            ) for b in books
        ]

    @staticmethod
    def UpdateBook(vb: ViewBook) -> List[str]:
        errs = ManageBook._validate(vb)
        if errs:
            return errs
        updated = Book(
            book_title=vb.title.strip(),
            book_author=vb.author.strip(),
            book_isbn=int(vb.isbn),
            book_genre=vb.genre.strip(),
            book_availability=vb.availability.strip(),
        )
        repo = BookRepo()
        try:
            repo.update_book(updated)
        finally:
            repo.close()
        return []

    @staticmethod
    def DeleteBook(vb: ViewBook) -> List[str]:
        if not vb.isbn.strip() or not vb.isbn.isdigit():
            return ["Valid ISBN is required to delete."]
        repo = BookRepo()
        try:
            repo.delete_book(int(vb.isbn))
        finally:
            repo.close()
        return []
