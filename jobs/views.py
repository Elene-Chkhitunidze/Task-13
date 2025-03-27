from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Job, JobApplication, FavoriteJob
from .forms import CustomUserCreationForm, JobForm
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from .forms import EmployerProfileForm, VacancyForm
from .models import EmployerProfile, Vacancy


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

            return redirect("home")  # Redirect job seekers elsewhere
    else:
        form = CustomUserCreationForm()
    return render(request, "jobs/register.html", {"form": form})


# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if user.user_type == 'employer':
                return redirect("employer_profile")  # Redirect employers to profile page
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'jobs/login.html', {'form': AuthenticationForm()})


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

# Job List View (with filtering by status)
def job_list(request):
    status_filter = request.GET.get('status')  # Get status from query params
    if status_filter:
        jobs = Job.objects.filter(status=status_filter)
    else:
        jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'status_filter': status_filter})

# Job Detail View
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

# Apply for Job View (Check if the deadline is passed)
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the job deadline has passed
    if job.deadline and job.deadline < timezone.now():
        messages.error(request, 'This job application deadline has passed.')
        return redirect('job_list')  # Redirect to job list if deadline is passed

    if request.method == "POST":
        cover_letter = request.POST.get('cover_letter')
        if cover_letter:
            JobApplication.objects.create(job=job, applicant=request.user, cover_letter=cover_letter)
            messages.success(request, 'Your application has been submitted!')
            return redirect('job_list')  # Redirect to job list after application
        else:
            messages.error(request, 'Cover letter is required!')
            return render(request, 'jobs/apply_job.html', {'job': job})
    return render(request, 'jobs/apply_job.html', {'job': job})

# Add Job to Favorites View
@login_required
def add_to_favorites(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # Check if the job is already in favorites for the user to avoid duplicates
    favorite, created = FavoriteJob.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, 'Job added to favorites!')
    else:
        messages.info(request, 'Job is already in your favorites.')
    return redirect('job_list')  # Redirect to job list after adding to favorites

# Favorite Jobs View
@login_required
def favorite_jobs(request):
    favorites = FavoriteJob.objects.filter(user=request.user)
    return render(request, 'jobs/favorites.html', {'favorites': favorites})

# Job Creation View (Only for Employers)
@login_required
def job_create(request):
    # Check if the user is an employer before allowing job creation
    if not request.user.user_type == 'employer':
        messages.error(request, "You need to be an employer to create a job listing.")
        return redirect('job_list')  # Redirect to job list if user is not an employer

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # Assign the current logged-in user as the employer
            job.save()
            messages.success(request, 'Job has been created successfully!')
            return redirect('job_list')  # Redirect to the job list page
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # მომხმარებელი გადამისამართდება ლოგინის გვერდზე