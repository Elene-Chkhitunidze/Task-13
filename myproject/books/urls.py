from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    BookListView, BookCreateView, BookDetailView, BookUpdateView, BookDeleteView,
    RegisterView, LoginView, LogoutView, BuyBookView, ChangePasswordView
)

urlpatterns = [
                  path('', BookListView.as_view(), name='book_list'),
                  path('add/', BookCreateView.as_view(), name='add_book'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('login/', LoginView.as_view(), name='login_'),
                  path('logout/', LogoutView.as_view(), name='logout_'),
                  path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
                  path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
                  path('books/<int:pk>/update/', BookUpdateView.as_view(), name='update_book'),
                  path('buy/<int:book_id>/', BuyBookView.as_view(), name='buy_book'),
                  path('change_password/', ChangePasswordView.as_view(), name='change_password'),
                  path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                  path('accounts/login/', LoginView.as_view(), name='login_'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
