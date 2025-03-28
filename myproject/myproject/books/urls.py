from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BookViewSet, GenreViewSet, OrderViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('books/', BookViewSet.as_view(), name='book-list'),
    path('books/<int:pk>/', BookViewSet.as_view(), name='book-detail'),
    path('genres/', GenreViewSet.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreViewSet.as_view(), name='genre-detail'),
    path('orders/', OrderViewSet.as_view(), name='order-list'),
    path('orders/buy/<int:book_id>/', OrderViewSet.as_view(), name='buy-book'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
