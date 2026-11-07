
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ViewBook:
    title: str = ""
    author: str = ""
    isbn: str = ""
    genre: str = ""
    availability: str = ""


@dataclass
class ViewMember:
    name: str = ""
    id: str = ""
    contact: str = ""
    type: str = ""


@dataclass
class Book:
    book_title: str = ""
    book_author: str = ""
    book_isbn: int = 0
    book_genre: str = ""
    book_availability: str = ""

    @staticmethod
    def from_row(row: Dict[str, Any]) -> "Book":
        return Book(
            book_title=row["book_title"],
            book_author=row["book_author"],
            book_isbn=row["book_isbn"],
            book_genre=row["book_genre"],
            book_availability=row["book_availability"],
        )


@dataclass
class Member:
    member_id: int = 0
    member_name: str = ""
    member_contact: str = ""
    member_type: str = ""

    @staticmethod
    def from_row(row: Dict[str, Any]) -> "Member":
        return Member(
            member_id=row["member_id"],
            member_name=row["member_name"],
            member_contact=row["member_contact"],
            member_type=row["member_type"],
        )
