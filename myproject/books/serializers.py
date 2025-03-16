from rest_framework import serializers
from .models import Book, Genre, Order


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'genre_id', 'published_date', 'description', 'cover_image']


class OrderSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'book', 'book_id', 'ordered_at']
