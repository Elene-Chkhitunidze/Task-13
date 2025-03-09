from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    published_date = models.DateField()
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
