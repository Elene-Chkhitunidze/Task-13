from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, EmployerProfileForm, VacancyForm, PasswordResetForm  # Import custom forms
from .models import EmployerProfile, Vacancy  # Import models


# Home view, handles role selection
def home(request):
    return render(request, 'jobs/home.html')  # Just render the home page template

# User Registration View
def register(request):
    # Handles user registration (both job seekers and employers)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user if the form is valid
            login(request, user)  # Log the user in after successful registration

            # Redirect based on user type (employer or job seeker)
            if user.user_type == 'employer':
                return redirect("employer_profile")  # Redirect employers to profile setup
            elif user.user_type == 'job_seeker':
                return redirect("job_seeker_profile")  # Redirect job seekers to their profile page
    else:
        form = CustomUserCreationForm()  # Instantiate an empty form

    return render(request, "jobs/register.html", {"form": form})  # Render the registration page


# Login View
def login_view(request):
    # Handles user login
    if request.method == 'POST':
        email = request.POST.get('username')  # Assuming 'username' is used for email input
        password = request.POST.get('password')  # Get password from form input

        # Authenticate user using email (custom authentication method)
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)  # Log the user in if authentication is successful

            # Redirect based on user type
            if user.user_type == 'employer':
                return redirect("employer_profile")  # Redirect to employer profile
            elif user.user_type == 'job_seeker':
                return redirect("job_seeker_profile")  # Redirect to job seeker profile
            return redirect("home")  # Redirect to the homepage if no user type is specified
        else:
            messages.error(request, "Invalid email or password")  # Display an error if login fails

    return render(request, 'jobs/login.html', {'form': AuthenticationForm()})  # Render login page with form


# Forgot Password View
def forgot_password(request):
    # Handles password reset process
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('new_password')

            try:
                User = get_user_model()
                user = User.objects.get(email=email)
                user.set_password(new_password)  # Set the new password
                user.save()
                messages.success(request, 'Your password has been successfully reset!')
                return redirect('login')  # Redirect to login page after resetting password
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist')  # Handle case when user is not found
        else:
            # If form is not valid, messages will be displayed via form errors
            pass
    else:
        form = PasswordResetForm()  # Instantiate an empty form

    return render(request, 'jobs/reset_password.html', {'form': form})  # Render password reset page


# Employer Profile View (Setup or Edit)
@login_required
def employer_profile(request):
    # Redirect non-employer users to the home page
    if not request.user.user_type == 'employer':
        return redirect('home')

    # Get or create an employer profile for the logged-in user
    profile, created = EmployerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)  # Handle form data and file uploads
        if form.is_valid():
            form.save()  # Save the employer profile if the form is valid
            return redirect('employer_profile_view')  # Redirect to the profile view after saving
        else:
            messages.error(request, "Please fill all required sections")  # Display error message if form is invalid
    else:
        form = EmployerProfileForm(instance=profile)  # Instantiate the form with existing data

    return render(request, 'jobs/employer_profile.html', {'form': form, 'profile': profile})  # Render profile page


# Employer Profile View (View Profile and Vacancies)
@login_required
def employer_profile_view(request):
    # Get the employer profile of the logged-in user
    profile = EmployerProfile.objects.get(user=request.user)
    vacancies = Vacancy.objects.filter(company=profile)  # Fetch the vacancies associated with the employer

    if request.method == 'POST' and 'logo' in request.FILES:
        profile.logo = request.FILES['logo']  # Handle logo upload
        profile.save()
        messages.success(request, "Logo uploaded successfully!")  # Success message after logo upload

    return render(request, 'jobs/employer_profile_view.html',
                  {'profile': profile, 'vacancies': vacancies})  # Render profile view page


# Add Vacancy (For Employers)
@login_required
def add_vacancy(request):
    # Allows employers to create a new job vacancy
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)  # Don't commit yet, we'll add the company
            vacancy.company = EmployerProfile.objects.get(user=request.user)  # Associate the vacancy with the employer
            vacancy.save()  # Save the vacancy to the database
            return redirect('employer_profile_view')  # Redirect to profile view after saving the vacancy
    else:
        form = VacancyForm()  # Instantiate an empty form

    return render(request, 'jobs/add_vacancy.html', {'form': form})  # Render add vacancy page


# Vacancy Detail View (For Job Seekers)
@login_required
def vacancy_detail(request, vacancy_id):
    # Fetch a specific vacancy by its ID
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    return render(request, 'jobs/vacancy_detail.html', {'vacancy': vacancy})  # Render the vacancy detail page


# Edit Vacancy (For Employers)
@login_required
def edit_vacancy(request, vacancy_id):
    # Allows employers to edit an existing vacancy
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)  # Prefill the form with the existing vacancy data
        if form.is_valid():
            form.save()  # Save the updated vacancy data
            return redirect('employer_profile_view')  # Redirect to employer profile view
    else:
        form = VacancyForm(instance=vacancy)  # Instantiate the form with the existing vacancy data

    return render(request, 'jobs/edit_vacancy.html', {'form': form, 'vacancy': vacancy})  # Render edit vacancy page


# Delete Vacancy (For Employers)
@login_required
def delete_vacancy(request, vacancy_id):
    # Allows employers to delete a specific vacancy
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    vacancy.delete()  # Delete the vacancy from the database
    return redirect('employer_profile_view')  # Redirect to employer profile view after deletion


# Custom Logout View
def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to the home page after logout


# Home View (Alternative)
def home_view(request):
    return render(request, 'home.html')  # Render the home page template


# Job Seeker Profile View (Vacancy Listings and Search)
@login_required
def job_seeker_profile(request):
    # Get search query parameters from the URL
    search_company = request.GET.get('search_company', '')
    search_title = request.GET.get('search_title', '')

    # Fetch all vacancies by default
    vacancies = Vacancy.objects.all()

    # Filter vacancies based on search queries
    if search_company:
        vacancies = vacancies.filter(company__icontains=search_company)
    if search_title:
        vacancies = vacancies.filter(title__icontains=search_title)

    # Implement pagination for vacancies (10 vacancies per page)
    paginator = Paginator(vacancies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass filtered and paginated vacancies to the template
    context = {
        'vacancies': page_obj,
        'search_company': search_company,
        'search_title': search_title
    }

    return render(request, 'jobs/job_seeker_profile.html', context)  # Render job seeker profile page


# Vacancy Detail View for Job Seekers (Apply for Jobs)
@login_required
def vacancy_detail_job_seeker(request, vacancy_id):
    # Fetch the vacancy details for job seekers
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    if request.method == 'POST':
        # Check if a resume is uploaded by the job seeker
        if 'resume' not in request.FILES:
            messages.error(request, "Please upload your resume!")  # Error if resume is missing

        # Save the uploaded resume and send an email application
        resume = request.FILES['resume']

        try:
            # Find the employer associated with the vacancy
            employer_profile = EmployerProfile.objects.get(company_name=vacancy.company)
            recipient_email = employer_profile.user.email

            # Compose the email with the resume attached
            from django.core.mail import EmailMessage
            email = EmailMessage(
                subject=f"Job Application for {vacancy.title}",
                body=f"""
                Dear Hiring Manager,

                I am applying for the position of {vacancy.title} at {vacancy.company}.

                Best regards,
                {request.user.username}
                """,
                from_email=request.user.email,
                to=[recipient_email],
            )

            # Attach the resume file to the email
            email.attach(resume.name, resume.read(), resume.content_type)

            try:
                # Attempt to send the email
                email.send(fail_silently=False)
                return redirect('resume_upload_success')  # Redirect to success page if email is sent

            except Exception as email_error:
                # Handle email sending error
                messages.error(request, f"Failed to send application: {str(email_error)}")

        except EmployerProfile.DoesNotExist:
            messages.error(request, "Could not find employer contact information.")  # Handle missing employer profile

    return render(request, 'jobs/vacancy_detail_job_seeker.html', {'vacancy': vacancy})  # Render vacancy details page


# Resume Upload Success Page (for Job Seekers)
@login_required
def resume_upload_success(request):
    return render(request, 'jobs/resume_upload_success.html')  # Render resume upload success page
