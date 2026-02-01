from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    books_count = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'email', 'bio', 'birth_date', 'books_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    

class AuthorListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    full_name = serializers.ReadOnlyField()
    books_count = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'email', 'books_count']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField()
    author_details = AuthorListSerializer(source='author', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'author_details',
            'isbn', 'genre', 'publication_date', 'pages', 'price',
            'description', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_isbn(self, value):
        """Custom ISBN validation"""
        if value and Book.objects.filter(isbn=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A book with this ISBN already exists.")
        return value

    def validate_pages(self, value):
        """Validate page count"""
        if value <= 0:
            raise serializers.ValidationError("Page count must be greater than 0.")
        return value


class BookListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    author_name = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'genre',
            'publication_date', 'price', 'is_available','description'
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for create/update operations"""
    
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'genre', 'publication_date',
            'pages', 'price', 'description', 'is_available'
        ]