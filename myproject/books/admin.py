from django.contrib import admin
from .models import Genre, Book
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Genre)
admin.site.register(Book)



def create_groups():

    admin_group, created = Group.objects.get_or_create(name='Administrator')
    if created:
        content_type = ContentType.objects.get_for_model(Book)
        permissions = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.set(permissions)


    default_group, created = Group.objects.get_or_create(name='Default')
    if created:
        content_type = ContentType.objects.get_for_model(Book)
        view_permission = Permission.objects.get(content_type=content_type, codename='view_book')
        default_group.permissions.add(view_permission)


create_groups()

