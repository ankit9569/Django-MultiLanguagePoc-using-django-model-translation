import django_filters
from django.db.models import Q

from .models import Author, Book


class AuthorFilter(django_filters.FilterSet):
    """FilterSet for Author model - used with DjangoFilterBackend"""
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Author
        fields = []

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )


class BookFilter(django_filters.FilterSet):
    """FilterSet for Book model - used with DjangoFilterBackend"""
    search = django_filters.CharFilter(method='filter_search', label='Search')
    genre = django_filters.ChoiceFilter(choices=Book.GENRE_CHOICES)
    author = django_filters.NumberFilter(field_name='author__id')
    available = django_filters.BooleanFilter(method='filter_available', label='Available only')

    class Meta:
        model = Book
        fields = ['genre', 'author']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) |
            Q(author__first_name__icontains=value) |
            Q(author__last_name__icontains=value) |
            Q(isbn__icontains=value)
        )

    def filter_available(self, queryset, name, value):
        if value in (True, 'true', '1'):
            return queryset.filter(is_available=True)
        return queryset
