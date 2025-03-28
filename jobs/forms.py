from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import EmployerProfile, Vacancy
from django.contrib.auth import get_user_model


# Custom form for user registration with extended validation and custom fields
class CustomUserCreationForm(UserCreationForm):
    # Meta class defines which model and fields are used in the form
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

    # Create a password confirmation field with a password input widget
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Validates the username to ensure it only contains letters (no digits or special characters)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isalpha():
            raise ValidationError(
                _('Username can only contain letters'))  # Raise error if username contains non-alphabetical characters
        return username

    # Validates the first password field to ensure it meets certain strength criteria (min length, contains digits, and uppercase)
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long'))  # Enforce minimum password length
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit'))  # Ensure the password has a number
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _('Password must contain at least one uppercase letter'))  # Ensure the password has an uppercase letter
        return password

    # Validates that both password fields (password1 and password2) match
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError(
                _('Passwords do not match. Please try again!'))  # Raise error if the passwords do not match
        return password2

    # Validates the email to ensure it's unique and that it follows the correct email format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use")  # Ensure email is unique
        return email

    # Ensures that the user selects a user type (Jon Seeker or Employer)
    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if not user_type:
            raise ValidationError(_('Please select a user type'))  # Raise error if user type is not selected
        return user_type


# Form for password reset, including validation and error handling
class PasswordResetForm(forms.Form):
    # Email field to request a password reset
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': _('Email is required'),
            'invalid': _('Enter a valid email address')
        }
    )

    # New password field to input the new password
    new_password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': _('New password is required')
        }
    )

    # Confirm password field to ensure the user re-enters the new password correctly
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': _('Confirmation password is required')
        }
    )

    # Validates the email input to check if the email is registered and in correct format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()

        # Ensure email is provided
        if not email:
            raise ValidationError(_('Email is required'))

        # Check if the email exists in the database
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                _('This email address is not registered. Please check and try again!'))  # Raise error if email is not found

        return email

    # Validates the new password to ensure it meets the password strength criteria
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')

        # Check for password length
        if len(password) < 8:
            raise ValidationError(
                _('Password must be at least 8 characters long'))  # Ensure the password has at least 8 characters

        # Ensure the password contains at least one digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit'))

        # Ensure the password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least one uppercase letter'))

        return password

    # Ensures that the new password and the confirmation password match
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Raise error if passwords do not match
        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError({
                'confirm_password': _('Passwords do not match. Please try again!')
            })

        return cleaned_data


# Form for creating or updating an employer profile, with validation on company name
class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'location', 'description', 'logo']

        logo = forms.ImageField(required=True)  # Logo is a required field

    # Validates the company name to ensure it's provided
    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if not company_name:
            raise forms.ValidationError("Company name is required")  # Raise error if company name is empty
        return company_name


# Form for creating or updating a job vacancy, with mandatory fields for company, title, and description
class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['company', 'title', 'description']

    company = forms.CharField(max_length=255, required=True)  # Ensure company is a required field
    title = forms.CharField(max_length=255, required=True)  # Ensure title is a required field
    description = forms.CharField(widget=forms.Textarea, required=True)  # Ensure description is a required field


# Simple form for searching job vacancies by title or company
class JobSearchForm(forms.Form):
    title = forms.CharField(required=False, label="Search by Title")  # Optional search by job title
    company = forms.CharField(required=False, label="Search by Company")  # Optional search by company


