from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Book, Genre, Order
from .serializers import BookSerializer, GenreSerializer, OrderSerializer
from .permissions import IsAdminOrReadOnly


## ჟანრების API
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


## წიგნების API
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


## შეკვეთები (მხოლოდ ავტორიზებულ მომხმარებლებს)
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        order = Order.objects.create(user=request.user, book=book)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
