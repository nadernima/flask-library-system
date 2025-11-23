# Database Schema

## Tables
- **users**
  - `id` (PK, integer)
  - `email` (string, unique, indexed)
  - `name` (string)
  - `role` (string: member | librarian | admin)
  - `password_hash` (string)
- **books**
  - `id` (PK, integer)
  - `title` (string, indexed)
  - `author` (string, indexed)
  - `year` (integer, indexed)
  - `language` (string, indexed)
  - `isbn` (string, unique, indexed)
  - `description` (text)
  - `copies_total` (integer)
  - `copies_available` (integer)
- **loans**
  - `id` (PK, integer)
  - `user_id` (FK → users.id, indexed)
  - `book_id` (FK → books.id, indexed)
  - `checkout_date` (datetime)
  - `due_date` (datetime)
  - `return_date` (datetime, nullable)

## Relationships
- A user can have many loans; deleting a user requires handling dependent loans manually.
- A book can have many loans and tracks availability via `copies_available`.
- Each loan belongs to one user and one book; `return_date` being null indicates the loan is still active.

## Notes
- Defaults: `copies_total`/`copies_available` default to 1; loan due dates default to checkout +14 days.
- SQLite is used by default; swap `DATABASE_URL` for other engines if needed.
