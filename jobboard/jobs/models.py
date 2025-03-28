from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)

    # Employer-specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_location = models.CharField(max_length=255, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Add related_name for groups and user_permissions to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoid conflict with the default User model
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoid conflict with the default User model
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='logos/', blank=False, null=False)  # Ensure file upload works

    def __str__(self):
        return self.company_name

class Vacancy(models.Model):
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField(null=True, blank=True)  # Optional explicit email field

    def __str__(self):
        return self.title

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

