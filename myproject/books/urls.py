from django.urls import path
from .views import book_list, add_book

urlpatterns = [
    path('', book_list, name='book_list'),
    path('add/', add_book, name='add_book'),
]