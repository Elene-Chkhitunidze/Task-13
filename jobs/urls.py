from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import custom_logout

urlpatterns = [
                  path('', views.home, name='home'),
                  path('jobs/', views.job_list, name='job_list'),
                  path('job/<int:job_id>/', views.job_detail, name='job_detail'),
                  path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
                  path('favorite/<int:job_id>/', views.add_to_favorites, name='add_to_favorites'),
                  path('favorites/', views.favorite_jobs, name='favorite_jobs'),
                  path('login/', views.login_view, name='login'),
                  path('register/', views.register, name='register'),

                  path('job/create/', views.job_create, name='job_create'),

                  # 🔹 Add the missing employer profile URL
                  path('employer-profile/', views.employer_profile, name='employer_profile'),
                  path('add-vacancy/', views.add_vacancy, name='add_vacancy'),
                  path('edit-vacancy/<int:vacancy_id>/', views.edit_vacancy, name='edit_vacancy'),
                  path('delete-vacancy/<int:vacancy_id>/', views.delete_vacancy, name='delete_vacancy'),
                  path('employer-profile/view/', views.employer_profile_view, name='employer_profile_view'),
                  path('vacancy/<int:vacancy_id>/', views.vacancy_detail, name='vacancy_detail'),
                  path('logout/', custom_logout, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
