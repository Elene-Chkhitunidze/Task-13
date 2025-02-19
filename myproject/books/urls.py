from django.urls import path
from .views import book_list, add_book, register, login_, logout_

urlpatterns = [
    path('', book_list, name='book_list'),
    path('add/', add_book, name='add_book'),
    path('register/', register, name='register'),
    path('login/', login_, name='login_'),
    path('logout/', logout_, name='logout_'),
]
