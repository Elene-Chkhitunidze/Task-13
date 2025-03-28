from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# CustomUser class extends Django's AbstractUser to include additional fields specific to your app
class CustomUser(AbstractUser):
    # Define the available user types for the user
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),  # User type for job seekers
        ('employer', 'Employer'),  # User type for employers
    )

    # user_type field determines if the user is a job seeker or an employer
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # The email field is made unique to ensure no two users can have the same email
    email = models.EmailField(unique=True)

    # Employer-specific fields: Optional fields to store employer-related information
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Employer's company name
    company_location = models.CharField(max_length=255, blank=True, null=True)  # Employer's company location
    company_description = models.TextField(blank=True, null=True)  # Description of the employer's company

    # Set the primary unique identifier to be the email field instead of the username
    USERNAME_FIELD = 'email'

    # Specify that 'username' is a required field during user creation (since 'email' is the primary key)
    REQUIRED_FIELDS = ['username']

    # Add Many-to-Many relationships for groups and permissions to avoid conflicts with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoid conflict with the default User model's group relationship
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoid conflict with the default User model's permissions relationship
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # String representation of the user instance, returns the username
    def __str__(self):
        return self.username


# EmployerProfile class stores additional information about employers
class EmployerProfile(models.Model):
    # One-to-One relationship with CustomUser (an employer will have only one profile)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')

    # Fields to store employer's company name, location, description, and logo
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='logos/', blank=False, null=False)  # Store company logo, required field

    # String representation of the employer profile, returns the company name
    def __str__(self):
        return self.company_name


# Vacancy class represents a job vacancy posted by an employer
class Vacancy(models.Model):
    # Basic fields for the job vacancy, including company name, job title, job description, and an optional contact email
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    contact_email = models.EmailField(null=True,
                                      blank=True)  # Optional field for the employer to provide a contact email

    # String representation of the vacancy, returns the job title
    def __str__(self):
        return self.title


# JobSeekerProfile class stores information specific to job seekers
class JobSeekerProfile(models.Model):
    # One-to-One relationship with the user (each job seeker will have one profile)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Optional field for the job seeker's resume, allowing file uploads
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    # String representation of the job seeker's profile, returns the job seeker's username
    def __str__(self):
        return f"{self.user.username}'s Profile"
