from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Book, Order
from .forms import BookForm
from .logs import log_action
from django.http import HttpResponseForbidden


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(title__icontains=query) if query else Book.objects.all()


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('book_list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/update_book.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(f'Book "{self.object.title}" updated by {self.request.user}')
        return response


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        log_action(f'Book "{book.title}" deleted by {request.user}')
        return super().delete(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = 'books/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        user = form.save()
        default_group, _ = Group.objects.get_or_create(name='Default')
        user.groups.add(default_group)
        login(self.request, user)
        return super().form_valid(form)


class LoginView(View):
    template_name = 'books/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
        return render(request, self.template_name, {'error': 'Invalid Credentials'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_')


class BuyBookView(View):
    def post(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('login_')

        book = get_object_or_404(Book, id=book_id)
        order = Order.objects.create(user=request.user, book=book)
        self.send_order_email(request.user, book)
        return redirect('book_list')

    def send_order_email(self, user, book):
        subject = 'Order Confirmation'
        message = f'Thank you {user.username}, you have successfully purchased {book.title}.'
        send_mail(subject, message, 'your_email@gmail.com', [user.email])


class ChangePasswordView(FormView):
    template_name = 'books/change_password.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect('book_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ResetPasswordView(FormView):
    template_name = 'books/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        form.save(request=self.request, from_email=settings.DEFAULT_FROM_EMAIL)
        return super().form_valid(form)


@receiver(post_save, sender=User)
def add_user(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name='Default')
        instance.groups.add(default_group)
