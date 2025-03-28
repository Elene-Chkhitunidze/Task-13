from django.contrib import admin
from .models import Genre, Book
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Genre)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_date')
    search_fields = ('title',)
    list_filter = ('genre',)

admin.site.register(Book, BookAdmin)

def create_groups():
    admin_group, created = Group.objects.get_or_create(name='Administrator')
    if created:
        content_type_book = ContentType.objects.get_for_model(Book)
        content_type_genre = ContentType.objects.get_for_model(Genre)
        permissions = Permission.objects.filter(content_type__in=[content_type_book, content_type_genre])
        admin_group.permissions.set(permissions)

    default_group, created = Group.objects.get_or_create(name='Default')
    if created:
        content_type = ContentType.objects.get_for_model(Book)
        view_permission = Permission.objects.get(content_type=content_type, codename='view_book')
        default_group.permissions.add(view_permission)

create_groups()
