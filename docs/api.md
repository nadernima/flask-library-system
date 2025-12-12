# Library Management System API

Text-only API reference for the Flask app. All endpoints sit under the `/api` prefix and require an authenticated session (Flask-Login session cookie). Roles apply where noted.

## Schemas

### Book
- `id` (integer)
- `title` (string)
- `author` (string)
- `year` (integer)
- `language` (string)
- `isbn` (string)
- `copies_total` (integer)
- `copies_available` (integer)

### Loan
- `loan_id` (integer)
- `book_id` (integer)
- `user_id` (integer)
- `checkout_date` (ISO datetime)
- `due_date` (ISO datetime)
- `return_date` (ISO datetime, nullable)

### Error
- `error` (string)

## Endpoints

### GET /api/books
List books (optional text search on title/author via `q`).

Query params:
- `q` (string, optional)

Response 200:
```json
[
  {
    "id": 1,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937,
    "language": "EN",
    "isbn": "978-0547928227",
    "copies_available": 3
  }
]
```

### POST /api/books (librarian/admin)
Create a book. Authenticated + librarian/admin role required.

Request body (application/json):
```json
{
  "title": "New Book",
  "author": "Author Name",
  "year": 2024,
  "language": "EN",
  "isbn": "1234567890",
  "description": "Optional",
  "copies_total": 2,
  "copies_available": 2
}
```

Response 201:
```json
{ "id": 42 }
```

Response 403: forbidden when not librarian/admin.

### POST /api/loans/{book_id}/checkout
Checkout a book for the current user.

Path params:
- `book_id` (integer)

Response 200:
```json
{ "loan_id": 10, "due_date": "2024-06-01T00:00:00Z" }
```

Response 400:
```json
{ "error": "No copies available" }
```

### POST /api/loans/{loan_id}/return
Return a loaned book. Must belong to the current user or a librarian/admin.

Path params:
- `loan_id` (integer)

Response 200:
```json
{ "returned": true }
```

Response 403: forbidden if not your loan and not librarian/admin.

## Notes
- Authentication is session-cookie based; use the web login to establish a session before hitting these endpoints.
- Errors return JSON with an `error` field and an appropriate HTTP status.
