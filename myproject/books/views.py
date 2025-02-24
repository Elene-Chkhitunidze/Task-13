from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseForbidden

def book_list(request):
    query = request.GET.get('q')
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            default_group, _ = Group.objects.get_or_create(name='Default')
            user.groups.add(default_group)
            login(request, user)
            return redirect('book_list')
    else:
        form = Register()
    return render(request, 'books/register.html', {'form': form})

def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
        return render(request, 'books/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'books/login.html')

def logout_(request):
    logout(request)
    return redirect('login_')

@receiver(post_save, sender=User)
def add_user(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name='Default')
        instance.groups.add(default_group)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    return render(request, 'books/book_detail.html', context)

@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')