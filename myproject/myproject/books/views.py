from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Book, Genre, Order
from .serializers import BookSerializer, GenreSerializer, OrderSerializer
from .permissions import IsAdminOrReadOnly

## ჟანრების API (CRUD)
class GenreViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

## წიგნების API (CRUD)
class BookViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

## შეკვეთების API (მხოლოდ ავტორიზებულ მომხმარებლებს)
class OrderViewSet(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs['book_id'])
        serializer.save(user=self.request.user, book=book)
