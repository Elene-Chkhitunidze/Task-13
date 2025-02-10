from tkinter.font import names

from django.urls import path
from sqlalchemy.dialects.mssql.information_schema import views

from .views import index
from . import views

urlpatterns = [
    path('index/', index, name='index'),
    path('render_/', views.render_, name='render_'),
]