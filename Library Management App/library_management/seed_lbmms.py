#!/usr/bin/env python3
"""
Seeder for LBMMS (Library Management) demo data.

- Inserts 100 Members and 100 Books using your existing repo classes.
- Safe to run multiple times: Members auto-increment IDs; Book ISBNs are stable and INSERTs will be skipped if they already exist.
- Keep this file at the project root (next to the 'infrastructure' and 'domain' folders).
- Run:  python seed_lbmms.py
"""

import sys
import random
from pathlib import Path

# --- Make package imports work when running this file from project root ---
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Import your repos and models ---
try:
    from infrastructure.db.member_repo import MemberRepo
    from infrastructure.db.book_repo import BookRepo
    from domain.models import Member, Book
except Exception as e:
    print("Import error:", e)
    print("Tip: place this file at the project root so imports like 'infrastructure.db.*' work.")
    sys.exit(1)


def rand_phone() -> str:
    # South African-ish mobile numbers for realism
    prefixes = ["060", "061", "062", "063", "064", "065", "066", "067", "068", "069", "071", "072", "073", "074", "076", "078", "079", "081", "082", "083", "084"]
    return f"{random.choice(prefixes)} {random.randint(100,999)} {random.randint(1000,9999)}"


def generate_members(n: int) -> list[Member]:
    first_names = [
        "Lerato","Thabo","Naledi","Kagiso","Sipho","Zanele","Aisha","Johan","Mia","Daniel",
        "Amelia","Lucas","Noah","Ava","Emily","Liam","Ethan","Olivia","Isabella","James",
        "Grace","Chloe","Mason","Aria","Benjamin","Emma","Elijah","Sophia","Zoë","Kayla"
    ]
    surnames = [
        "Mokoena","Naidoo","van der Merwe","Nkosi","Dlamini","Pillay","Smith","Botha","Khumalo","Molefe",
        "Williams","Pretorius","Chauke","Zulu","Jansen","Sithole","Brown","de Klerk","Fourie","Mthembu",
        "Mabaso","Jordaan","Nel","van Wyk","Ngcobo","du Plessis","Radebe","Coetzee","Meyiwa","Kruger"
    ]
    types = ["Student","Adult","Senior","Staff"]

    members: list[Member] = []
    for _ in range(n):
        name = f"{random.choice(first_names)} {random.choice(surnames)}"
        # Mix phone and very simple email for demo variety
        if random.random() < 0.55:
            contact = rand_phone()
        else:
            email_user = name.lower().replace(" ", ".").replace("ö","o").replace("ë","e").replace("é","e")
            contact = f"{email_user}@example.org"
        member_type = random.choice(types)
        # Let DB auto-assign member_id by passing force_id=False in repo call
        members.append(Member(member_id=None, member_name=name, member_contact=contact, member_type=member_type))
    return members


def generate_books(n: int) -> list[Book]:
    adjectives = ["Hidden","Lost","Silent","Golden","Crimson","Electric","Ancient","Wild","Gentle","Broken",
                  "Brave","Sacred","Forgotten","Endless","Secret","Distant","Luminous","Faded","Midnight","Whispering"]
    nouns = ["Garden","Empire","River","City","Forest","Promise","Storm","Journey","Echo","Library",
             "Door","Harbour","Machine","Song","Map","Trial","Road","Mirror","Sky","Archive"]
    authors_first = ["John","Sarah","Thando","Michael","Aisha","Catherine","Sipho","Emma","Daniel","Lerato",
                     "Noah","Olivia","Ethan","Mia","Ava","James","Grace","Liam","Emily","Lucas"]
    authors_last = ["Meyer","Khan","Dlamini","Brown","Naidoo","Smit","Botha","Ngcobo","Williams","Kruger",
                    "Radebe","Pillay","Nkosi","Fourie","Coetzee","Pretorius","Chauke","Mokoena","van Wyk","Jordaan"]
    genres = ["Fiction","Non-Fiction","Mystery","Sci-Fi","Fantasy","Romance","Thriller","History","Biography","Young Adult"]
    availability_values = ["Available","Checked Out"]

    # Stable 13-digit ISBN base to avoid collisions across runs; increment by 1
    isbn_start = 9780306400000  # classic-looking prefix; integer fits in SQLite
    books: list[Book] = []
    used_titles = set()

    i = 0
    while len(books) < n:
        title = f"{random.choice(adjectives)} {random.choice(nouns)}"
        if title in used_titles:
            continue
        used_titles.add(title)

        author = f"{random.choice(authors_first)} {random.choice(authors_last)}"
        genre = random.choice(genres)
        availability = random.choices(availability_values, weights=[75, 25], k=1)[0]  # mostly available
        isbn = isbn_start + i
        i += 1

        books.append(Book(book_title=title, book_author=author, book_isbn=isbn,
                          book_availability=availability, book_genre=genre))
    return books


def seed_members(n: int = 100) -> int:
    repo = MemberRepo()
    added = 0
    try:
        for m in generate_members(n):
            # Let DB pick the ID
            repo.insert_member(m, force_id=False)
            added += 1
    finally:
        repo.close()
    return added


def seed_books(n: int = 100) -> int:
    repo = BookRepo()
    added = 0
    try:
        for b in generate_books(n):
            try:
                repo.insert_book(b)
                added += 1
            except Exception as ex:
                # Likely a duplicate ISBN; skip quietly so the script can be re-run
                # You can print(ex) for debugging if needed.
                pass
    finally:
        repo.close()
    return added


def main():
    random.seed(361)  # deterministic but still "random-looking"
    m = seed_members(100)
    b = seed_books(100)
    print(f"✅ Seed complete: {m} members, {b} books inserted.")


if __name__ == "__main__":
    main()
