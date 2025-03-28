from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse

from .forms import EmployerProfileForm, VacancyForm, PasswordResetForm, JobApplicationForm, JobSeekerProfile
from .models import EmployerProfile

from django.contrib import messages

from django.contrib.auth import get_user_model

from .models import Vacancy


from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

def home(request):
    if request.method == "POST":
        role = request.POST.get('role')
        if role == 'job_seeker':
            return HttpResponse("თქვენ აირჩიეთ: სამსახურის მაძიებელი")
        elif role == 'employer':
            return HttpResponse("თქვენ აირჩიეთ: დამსაქმებელი")
    return render(request, 'jobs/home.html')


# User Registration View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.user_type == 'employer':
                return redirect("employer_profile")  # Redirect employers to profile setup
            elif user.user_type == 'job_seeker':
                return redirect("job_seeker_profile")  # Redirect job seekers to job seeker page
    else:
        form = CustomUserCreationForm()

    return render(request, "jobs/register.html", {"form": form})

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Assuming 'username' is used for email input
        password = request.POST.get('password')

        # Authenticate using email (CustomUser model uses email as the username)
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if user.user_type == 'employer':
                return redirect("employer_profile")  # Redirect employers to profile page
            elif user.user_type == 'job_seeker':
                return redirect("job_seeker_profile")  # Redirect job seekers to their page
            return redirect("home")  # Or redirect to a general homepage
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'jobs/login.html', {'form': AuthenticationForm()})

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('new_password')

            try:
                User = get_user_model()
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been successfully reset!')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
        else:
            # If form is not valid, messages will be displayed via form errors
            pass
    else:
        form = PasswordResetForm()

    return render(request, 'jobs/reset_password.html', {'form': form})

@login_required
def employer_profile(request):
    if not request.user.user_type == 'employer':
        return redirect('home')  # Redirect non-employers

    # Get or create employer profile
    profile, created = EmployerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)  # Add request.FILES to handle logo uploads
        if form.is_valid():
            form.save()
              # Success message
            return redirect('employer_profile_view')  # Redirect to profile page
        else:
            messages.error(request, "Please fill all required sections.")  # Error message if form is invalid
    else:
        form = EmployerProfileForm(instance=profile)

    return render(request, 'jobs/employer_profile.html', {'form': form, 'profile': profile})


@login_required
def employer_profile_view(request):
    profile = EmployerProfile.objects.get(user=request.user)
    vacancies = Vacancy.objects.filter(company=profile)

    if request.method == 'POST' and 'logo' in request.FILES:
        profile.logo = request.FILES['logo']
        profile.save()
        messages.success(request, "Logo uploaded successfully!")

    return render(request, 'jobs/employer_profile_view.html', {'profile': profile, 'vacancies': vacancies})


@login_required
def add_vacancy(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = EmployerProfile.objects.get(user=request.user)
            vacancy.save()
            return redirect('employer_profile_view')
    else:
        form = VacancyForm()
    return render(request, 'jobs/add_vacancy.html', {'form': form})


@login_required
# View to display individual vacancy details
def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    return render(request, 'jobs/vacancy_detail.html', {'vacancy': vacancy})


@login_required
def edit_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            return redirect('employer_profile_view')
    else:
        form = VacancyForm(instance=vacancy)

    # 🔥 Fix: Pass `vacancy` to the template
    return render(request, 'jobs/edit_vacancy.html', {'form': form, 'vacancy': vacancy})

@login_required
def delete_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    vacancy.delete()
    return redirect('employer_profile_view')


def custom_logout(request):
    logout(request)
    return redirect('home')  # Or use '/' for home page

def home_view(request):
    return render(request, 'home.html')  # Render your home page template



# Job Seeker Profile View
@login_required
def job_seeker_profile(request):
    # Get the search query parameters
    search_company = request.GET.get('search_company', '')
    search_title = request.GET.get('search_title', '')

    # Fetch all vacancies by default
    vacancies = Vacancy.objects.all()

    # Filter vacancies based on search queries
    if search_company:
        vacancies = vacancies.filter(company__icontains=search_company)
    if search_title:
        vacancies = vacancies.filter(title__icontains=search_title)

    # Implement pagination
    paginator = Paginator(vacancies, 10)  # Show 10 vacancies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vacancies': page_obj,
        'search_company': search_company,
        'search_title': search_title
    }

    return render(request, 'jobs/job_seeker_profile.html', context)

@login_required
def vacancy_detail_job_seeker(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    # Get or create JobSeekerProfile for the current user
    job_seeker_profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Check if resume is uploaded
        if 'resume' not in request.FILES:
            messages.error(request, "Please upload your resume!")
            return render(request, 'jobs/vacancy_detail_job_seeker.html', {'vacancy': vacancy})

        # Save the uploaded resume
        resume = request.FILES['resume']
        job_seeker_profile.resume = resume
        job_seeker_profile.save()

        try:
            # Find the employer profile associated with the vacancy's company
            try:
                employer_profile = EmployerProfile.objects.get(company_name=vacancy.company)
                recipient_email = employer_profile.user.email  # Get the email of the user who created the profile
            except EmployerProfile.DoesNotExist:
                messages.error(request, "Could not find employer contact information.")
                return render(request, 'jobs/vacancy_detail_job_seeker.html', {'vacancy': vacancy})

            # Prepare email
            subject = f"Job Application for {vacancy.title}"

            # Compose email body
            email_body = f"""
            Dear Hiring Manager,

            I am applying for the position of {vacancy.title} at {vacancy.company}.

            Best regards,
            {request.user.username}
            """

            # Create email message
            from django.core.mail import send_mail

            try:
                send_mail(
                    subject=subject,
                    message=email_body,
                    from_email=request.user.email,
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )
                # Redirect to new success page
                return redirect('resume_upload_success')

            except Exception as email_error:
                # Log the full error details
                import traceback
                print(f"Email sending error: {email_error}")
                traceback.print_exc()
                messages.error(request, f"Failed to send application: {str(email_error)}")

        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")

    return render(request, 'jobs/vacancy_detail_job_seeker.html', {'vacancy': vacancy})

@login_required
def resume_upload_success(request):
    return render(request, 'jobs/resume_upload_success.html')