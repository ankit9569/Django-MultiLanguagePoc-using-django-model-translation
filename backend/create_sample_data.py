# #!/usr/bin/env python
# """
# Script to create sample data for testing the Library Management System
# """
# import os
# import sys
# import django
# from datetime import date, datetime

# # Setup Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

# from apps.library.models import Author, Book

# def create_sample_data():
#     """Create sample authors and books for testing"""
    
#     print("Creating sample data...")
    
#     # Create Authors
#     authors_data = [
#         {
#             'first_name': 'J.K.',
#             'last_name': 'Rowling',
#             'email': 'jk.rowling@example.com',
#             'bio': 'British author, best known for the Harry Potter series.',
#             'birth_date': date(1965, 7, 31)
#         },
#         {
#             'first_name': 'George',
#             'last_name': 'Orwell',
#             'email': 'george.orwell@example.com',
#             'bio': 'English novelist and essayist, journalist and critic.',
#             'birth_date': date(1903, 6, 25)
#         },
#         {
#             'first_name': 'Agatha',
#             'last_name': 'Christie',
#             'email': 'agatha.christie@example.com',
#             'bio': 'English writer known for her detective novels.',
#             'birth_date': date(1890, 9, 15)
#         },
#         {
#             'first_name': 'Stephen',
#             'last_name': 'King',
#             'email': 'stephen.king@example.com',
#             'bio': 'American author of horror, supernatural fiction, suspense, and fantasy novels.',
#             'birth_date': date(1947, 9, 21)
#         },
#         {
#             'first_name': 'Jane',
#             'last_name': 'Austen',
#             'email': 'jane.austen@example.com',
#             'bio': 'English novelist known primarily for her six major novels.',
#             'birth_date': date(1775, 12, 16)
#         }
#     ]
    
#     authors = []
#     for author_data in authors_data:
#         author, created = Author.objects.get_or_create(
#             email=author_data['email'],
#             defaults=author_data
#         )
#         authors.append(author)
#         if created:
#             print(f"Created author: {author.full_name}")
#         else:
#             print(f"Author already exists: {author.full_name}")
    
#     # Create Books
#     books_data = [
#         {
#             'title': "Harry Potter and the Philosopher's Stone",
#             'author': authors[0],  # J.K. Rowling
#             'isbn': '9780747532699',
#             'genre': 'fantasy',
#             'publication_date': date(1997, 6, 26),
#             'pages': 223,
#             'price': 12.99,
#             'description': 'The first book in the Harry Potter series.',
#             'is_available': True
#         },
#         {
#             'title': "Harry Potter and the Chamber of Secrets",
#             'author': authors[0],  # J.K. Rowling
#             'isbn': '9780747538493',
#             'genre': 'fantasy',
#             'publication_date': date(1998, 7, 2),
#             'pages': 251,
#             'price': 13.99,
#             'description': 'The second book in the Harry Potter series.',
#             'is_available': True
#         },
#         {
#             'title': '1984',
#             'author': authors[1],  # George Orwell
#             'isbn': '9780451524935',
#             'genre': 'sci_fi',
#             'publication_date': date(1949, 6, 8),
#             'pages': 328,
#             'price': 14.99,
#             'description': 'A dystopian social science fiction novel.',
#             'is_available': True
#         },
#         {
#             'title': 'Animal Farm',
#             'author': authors[1],  # George Orwell
#             'isbn': '9780451526342',
#             'genre': 'fiction',
#             'publication_date': date(1945, 8, 17),
#             'pages': 112,
#             'price': 10.99,
#             'description': 'An allegorical novella about farm animals.',
#             'is_available': False
#         },
#         {
#             'title': 'Murder on the Orient Express',
#             'author': authors[2],  # Agatha Christie
#             'isbn': '9780062693662',
#             'genre': 'mystery',
#             'publication_date': date(1934, 1, 1),
#             'pages': 256,
#             'price': 11.99,
#             'description': 'A detective novel featuring Hercule Poirot.',
#             'is_available': True
#         },
#         {
#             'title': 'The Shining',
#             'author': authors[3],  # Stephen King
#             'isbn': '9780307743657',
#             'genre': 'mystery',
#             'publication_date': date(1977, 1, 28),
#             'pages': 447,
#             'price': 15.99,
#             'description': 'A horror novel about the Overlook Hotel.',
#             'is_available': True
#         },
#         {
#             'title': 'Pride and Prejudice',
#             'author': authors[4],  # Jane Austen
#             'isbn': '9780141439518',
#             'genre': 'romance',
#             'publication_date': date(1813, 1, 28),
#             'pages': 432,
#             'price': 9.99,
#             'description': 'A romantic novel of manners.',
#             'is_available': True
#         },
#         {
#             'title': 'Emma',
#             'author': authors[4],  # Jane Austen
#             'isbn': '9780141439587',
#             'genre': 'romance',
#             'publication_date': date(1815, 12, 23),
#             'pages': 474,
#             'price': 10.99,
#             'description': 'A novel about youthful hubris and romantic misunderstandings.',
#             'is_available': False
#         }
#     ]
    
#     for book_data in books_data:
#         book, created = Book.objects.get_or_create(
#             isbn=book_data['isbn'],
#             defaults=book_data
#         )
#         if created:
#             print(f"Created book: {book.title}")
#         else:
#             print(f"Book already exists: {book.title}")
    
#     print(f"\nSample data creation complete!")
#     print(f"Total Authors: {Author.objects.count()}")
#     print(f"Total Books: {Book.objects.count()}")
#     print(f"Available Books: {Book.objects.filter(is_available=True).count()}")
#     print(f"Unavailable Books: {Book.objects.filter(is_available=False).count()}")

# if __name__ == '__main__':
#     create_sample_data()