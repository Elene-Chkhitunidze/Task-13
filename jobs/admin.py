from django.contrib import admin
from .models import CustomUser, Job, JobApplication, FavoriteJob

admin.site.register(CustomUser)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(FavoriteJob)
