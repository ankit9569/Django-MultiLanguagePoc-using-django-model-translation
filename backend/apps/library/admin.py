from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'books_count', 'created_at']
    list_filter = ['created_at', 'birth_date']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'books_count']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'birth_date')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
        ('Metadata', {
            'fields': ('books_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'genre', 'publication_date', 'price', 'is_available']
    list_filter = ['genre', 'is_available', 'publication_date', 'created_at']
    search_fields = ['title', 'author__first_name', 'author__last_name', 'isbn']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_available', 'price']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'genre')
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'pages', 'price', 'is_available')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_name(self, obj):
        return obj.author.full_name
    author_name.short_description = 'Author'