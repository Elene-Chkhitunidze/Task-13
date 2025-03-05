from django.urls import path
from .views import book_list, add_book, register, login_, logout_, book_detail, delete_book, update_book, buy_book, change_password, reset_password
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', book_list, name='book_list'),
    path('add/', add_book, name='add_book'),
    path('register/', register, name='register'),
    path('login/', login_, name='login_'),
    path('logout/', logout_, name='logout_'),
    path('books/<int:book_id>/', book_detail, name='book_detail'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
    path("books/<int:book_id>/update/", update_book, name="update_book"),
    path('buy/<int:book_id>/', buy_book, name='buy_book'),
    path('change_password/', change_password, name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/', login_, name='login_'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
