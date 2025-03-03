from django.urls import path
from .views import book_list, add_book, register, login_, logout_, book_detail, delete_book, update_book
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', book_list, name='book_list'),
    path('add/', add_book, name='add_book'),
    path('register/', register, name='register'),
    path('login/', login_, name='login_'),
    path('logout/', logout_, name='logout_'),
    path('books/<int:book_id>/', book_detail, name='book_detail'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
    path("books/<int:book_id>/update/", update_book, name="update_book"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
