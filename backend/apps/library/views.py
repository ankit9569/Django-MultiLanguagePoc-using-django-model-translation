from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q

from .models import Author, Book
from .serializers import (
    AuthorSerializer, AuthorListSerializer,
    BookSerializer, BookListSerializer, BookCreateUpdateSerializer
)
from .filters import AuthorFilter, BookFilter


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Author model.
    
    Additional actions:
    - books: Get all books by a specific author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        return AuthorSerializer

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Get all books by this author"""
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Custom delete with validation"""
        author = self.get_object()
        if author.books.exists():
            return Response(
                {'error': 'Cannot delete author with existing books. Delete books first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Return library statistics for dashboard"""
        book_stats = Book.objects.aggregate(
            total=Count('id'),
            available=Count('id', filter=Q(is_available=True)),
            unavailable=Count('id', filter=Q(is_available=False))
        )
        total_authors = Author.objects.count()
        genre_counts = Book.objects.values('genre').annotate(count=Count('id'))
        genres_distribution = {item['genre']: item['count'] for item in genre_counts}
        return Response({
            'total_authors': total_authors,
            'total_books': book_stats['total'],
            'available_books': book_stats['available'],
            'unavailable_books': book_stats['unavailable'],
            'genres_distribution': genres_distribution
        })

    @action(detail=False, methods=['get'])
    def genres(self, request):
        """Return genre choices for filter dropdown"""
        return Response([
            {'value': choice[0], 'label': choice[1]}
            for choice in Book.GENRE_CHOICES
        ])
