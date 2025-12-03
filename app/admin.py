from django.contrib import admin
from .models import Author, Genre, Publisher, Book, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'bio', 'birth_date', 'death_date')
    search_fields = ('last_name', 'first_name', 'bio')
    list_filter = ('birth_date', 'death_date')
    ordering = ('last_name', 'first_name')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'address')
    search_fields = ('name', 'website')
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publisher', 'published_date', 'isbn', 'pages')
    search_fields = ('title', 'author__last_name', 'author__first_name', 'publisher__name', 'isbn')
    list_filter = ('published_date', 'publisher', 'genres')
    ordering = ('title',)
    filter_horizontal = ('genres',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'reviewer_name', 'rating', 'created_at')
    search_fields = ('book__title', 'reviewer_name', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)