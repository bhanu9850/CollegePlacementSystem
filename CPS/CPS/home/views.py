from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Company, Drive, StudentProfile
from .forms import CompanyForm, DriveForm, StudentProfileForm
from django.contrib.auth.models import User
from django.utils.timezone import now
from .decorators import student_required, superuser_required

# Home View
def home(request):
    return render(request, 'home.html')

# Company Views
@superuser_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, "company/company_list.html", {"companies": companies})

@superuser_required
def company_detail(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        return render(request, "company/company_detail.html", {"company": company})
    except ObjectDoesNotExist:
        return redirect("company_list")

@superuser_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            form.save()
            messages.success(request, "Company Added succesfully.")
            return redirect("company_list")
    else:
        form = CompanyForm()
        messages.error(request, "Company created failed.")

    return render(request, "company/company_form.html", {"form": form})

@superuser_required
def company_update(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        if request.method == "POST":
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                messages.success(request, "Company Updated succesfully.")
                return redirect("company_list")
        else:
            form = CompanyForm(instance=company)
        return render(request, "company/company_form.html", {"form": form})
    except ObjectDoesNotExist:
        return redirect("company_list")

@superuser_required
def company_delete(request, pk):
    try:
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        messages.success(request, "Company Deleted succesfully.")
        return redirect("company_list")
    except ObjectDoesNotExist:
        return redirect("company_list")

# Drive Views
@superuser_required
def drive_list(request):
    drives = Drive.objects.all()
    return render(request, "drive/drive_list.html", {"drives": drives})

def active_drives(request):
    student = request.user.student_profile
    active_drives = Drive.objects.filter(application_deadline__gte=now().date())
    for drive in active_drives:
        drive.applied_by_current_user = student in drive.applied_students.all()
    return render(request, "drive/active_drives.html", {"active_drives": active_drives})

@superuser_required
def drive_detail(request, pk):
    try:
        drive = get_object_or_404(Drive, pk=pk)
        return render(request, "drive/drive_detail.html", {"drive": drive})
    except ObjectDoesNotExist:
        return redirect("drive_list")

@superuser_required
def drive_create(request):
    if request.method == "POST":
        form = DriveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Drive Created succesfully.")
            return redirect("drive_list")
    else:
        form = DriveForm()
    return render(request, "drive/drive_form.html", {"form": form})

@superuser_required
def drive_update(request, pk):
    try:
        drive = get_object_or_404(Drive, pk=pk)
        if request.method == "POST":
            form = DriveForm(request.POST, instance=drive)
            if form.is_valid():
                form.save()
                messages.success(request, "Drive Updated succesfully.")
                return redirect("drive_list")
        else:
            form = DriveForm(instance=drive)
        return render(request, "drive/drive_form.html", {"form": form})
    except ObjectDoesNotExist:
        return redirect("drive_list")

@superuser_required
def drive_delete(request, pk):
    try:
        drive = get_object_or_404(Drive, pk=pk)
        drive.delete()
        messages.success(request, "Company Deleted succesfully.")
        return redirect("drive_list")
    except ObjectDoesNotExist:
        return redirect("drive_list")

# Student Profile Views
@student_required
def create_student_profile(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Student profile created succesfully.")
            return redirect("student_dashboard")
    else:
        form = StudentProfileForm()
    return render(request, "student/student_profile.html", {"form": form})

@student_required
def student_profile_update(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = StudentProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Student profile Updated succesfully.")
                return redirect("student_dashboard")
        else:
            form = StudentProfileForm(instance=profile)
        return render(request, "student/student_profile.html", {"form": form})
    except ObjectDoesNotExist:
        return redirect("create_student_profile")

@student_required
def student_dashboard(request, student_id=None):
    try:
        profile = get_object_or_404(StudentProfile, id=student_id) if student_id else get_object_or_404(StudentProfile, user=request.user)
        applied_drives = Drive.objects.filter(applied_students=profile)
        return render(request, "student/student_dashboard.html", {"profile": profile, "applied_drives": applied_drives})
    except ObjectDoesNotExist:
        return redirect("create_student_profile")


@superuser_required
def select_student(request, drive_id, student_id):
    try:
        drive = get_object_or_404(Drive, id=drive_id)
        student = get_object_or_404(StudentProfile, id=student_id)

        if student in drive.selected_students.all():
            messages.warning(request, "Student is already selected for this drive.")
        else:
            drive.selected_students.add(student)
            messages.success(request, f"{student.user.get_full_name()} has been selected!")

        return redirect("drive_detail", pk=drive.pk)
    except ObjectDoesNotExist:
        return redirect("drive_list")

@student_required
def apply_drive(request, pk):
    try:
        drive = get_object_or_404(Drive, pk=pk)
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        drive.applied_students.add(student_profile)
        drive.save()
        messages.success(request, "Drive added succesfully.")
        return redirect("student_dashboard")
    except ObjectDoesNotExist:
        return redirect("active_drives")

@superuser_required
def applied_students(request, pk):
    try:
        drive = get_object_or_404(Drive, pk=pk)
        applied_students = drive.applied_students.all()
        return render(request, "student/applied_students.html", {"drive": drive, "students": applied_students})
    except ObjectDoesNotExist:
        return redirect("drive_list")

@superuser_required
def selected_students(request, pk):
    try:
        drive = get_object_or_404(Drive, pk=pk)
        selected_students = drive.selected_students.all()
        return render(request, "student/selected_students.html", {"drive": drive, "selected_students": selected_students})
    except ObjectDoesNotExist:
        return redirect("drive_list")

@superuser_required
def admin_dashboard(request):
    students_count = User.objects.filter(groups__name="Students").count()
    total_users = User.objects.count()
    active_drives = Drive.objects.filter(application_deadline__gte=now().date()).count()
    active_drives_list = Drive.objects.filter(application_deadline__gte=now().date())
    return render(request, 'admin_dashboard.html', {
        'students_count': students_count,
        'total_users': total_users,
        'active_drives': active_drives,
        'active_drives_list': active_drives_list
    })


@superuser_required
def company_dashboard(request):
    user = request.user
    print("The current user is:", user)

    try:
        company = Company.objects.get(user=user)  # Ensure Company has a `user` field
        print("The current company is:", company)
        print(company.name)
        company_drives = company.drives.all() # Use `.drive_set.all()` instead of `company.drives.all()`
        print("Company drives:", company_drives)

        applied_students = StudentProfile.objects.filter(applied_drives__in=company_drives).distinct()

        return render(request, 'company/company_dashboard.html', {
            'company':company,
            'company_drives': company_drives,
            'applied_students': applied_students
        })
    
    except ObjectDoesNotExist:
        messages.error(request, "Company profile not found for this user.")
        return redirect("home")

@superuser_required
def student_list(request):
    students_list = StudentProfile.objects.all()
    return render(request,'student/students_list.html',{"students_list":students_list})