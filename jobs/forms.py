from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Job
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import EmployerProfile, Vacancy
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2', 'user_type']
        labels = {
            'email': _('Email'),
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
            'user_type': _('User Type'),
        }
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
            'user_type': None,
        }

    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Validate username (no digits or special characters)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalpha():
            raise ValidationError(_('Username can only contain letters'))
        return username

    # Validate password (minimum length 8 characters, at least one uppercase letter and one digit)
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least one uppercase letter'))
        return password

    # Validate that both passwords match
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError(_('Passwords do not match. Please try again!'))
        return password2

    # Validate email to ensure it contains '@'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    # Ensure that the user_type is selected
    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if not user_type:
            raise ValidationError(_('Please select a user type'))
        return user_type


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'location', 'description', 'logo']

        logo = forms.ImageField(required=True)

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if not company_name:
            raise forms.ValidationError("Company name is required.")
        return company_name


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['company', 'title', 'description']

    company = forms.CharField(max_length=255, required=True)  # Ensure it's mandatory
    title = forms.CharField(max_length=255, required=True)  # Ensure it's mandatory
    description = forms.CharField(widget=forms.Textarea, required=True)  # Ensure it's mandatory

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'deadline', 'status']

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError(_("Deadline cannot be in the past!"))
        return deadline
