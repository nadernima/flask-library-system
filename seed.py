from app import create_app, db
from app.models import User, Book
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(email="admin@example.com", name="Admin", role="admin")
    admin.set_password("adminpass")
    librarian = User(email="librarian@example.com", name="Librarian", role="librarian")
    librarian.set_password("librarianpass")
    member = User(email="member@example.com", name="Member", role="member")
    member.set_password("memberpass")

    db.session.add_all([admin, librarian, member])

    sample_books = [
        # Admin-added (5)
        Book(title="The Pragmatic Programmer", author="Andrew Hunt; David Thomas",
             year=1999, language="EN", isbn="978-0201616224", copies_total=3, copies_available=3),
        Book(title="Clean Code", author="Robert C. Martin",
             year=2008, language="EN", isbn="978-0132350884", copies_total=2, copies_available=2),
        Book(title="Le Petit Prince", author="Antoine de Saint-Exupéry",
             year=1943, language="FR", isbn="978-0156013987", copies_total=4, copies_available=4),
        Book(title="Don Quixote", author="Miguel de Cervantes",
             year=1605, language="ES", isbn="978-0060934347", copies_total=2, copies_available=2),
        Book(title="Invisible Cities", author="Italo Calvino",
             year=1972, language="IT", isbn="978-0156453806", copies_total=3, copies_available=3),

        # Librarian-added (10)
        Book(title="Sapiens", author="Yuval Noah Harari",
             year=2011, language="EN", isbn="978-0062316097", copies_total=3, copies_available=3),
        Book(title="Thinking, Fast and Slow", author="Daniel Kahneman",
             year=2011, language="EN", isbn="978-0374533557", copies_total=2, copies_available=2),
        Book(title="Educated", author="Tara Westover",
             year=2018, language="EN", isbn="978-0399590504", copies_total=2, copies_available=2),
        Book(title="Norwegian Wood", author="Haruki Murakami",
             year=1987, language="JA", isbn="978-0375704024", copies_total=2, copies_available=2),
        Book(title="One Hundred Years of Solitude", author="Gabriel García Márquez",
             year=1967, language="ES", isbn="978-0060883287", copies_total=2, copies_available=2),
        Book(title="The Alchemist", author="Paulo Coelho",
             year=1988, language="PT", isbn="978-0061122415", copies_total=3, copies_available=3),
        Book(title="The Hobbit", author="J.R.R. Tolkien",
             year=1937, language="EN", isbn="978-0547928227", copies_total=3, copies_available=3),
        Book(title="1984", author="George Orwell",
             year=1949, language="EN", isbn="978-0451524935", copies_total=4, copies_available=4),
        Book(title="The Little Prince", author="Antoine de Saint-Exupéry",
             year=1943, language="FR", isbn="978-0156012195", copies_total=3, copies_available=3),
        Book(title="The Kite Runner", author="Khaled Hosseini",
             year=2003, language="EN", isbn="978-1594631931", copies_total=2, copies_available=2),
    ]
    db.session.add_all(sample_books)
    db.session.commit()
    print("Seeded database with users and books.")
