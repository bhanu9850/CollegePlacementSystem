from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('IT', 'IT'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Manufacturing', 'Manufacturing'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    industry_type = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)

    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Drive(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Internship', 'Internship'),
        ('Part-time', 'Part-time'),
    ]
    BACKLOG_CHOICES = [
        ('Yes','Yes'),
        ('NO','NO'),
    ]

    YEAR_CHOICES =[
        ('2023','2023'),
        ('2024','2024'),
        ('2025','2025'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="drives")
    job_role = models.CharField(max_length=255)
    job_description = models.TextField()
    salary_package = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    bond_period = models.PositiveIntegerField(blank=True, null=True, help_text="Duration in months")

    job_location = models.CharField(max_length=255)

    cgpa_requirement = models.DecimalField(max_digits=3, decimal_places=2, help_text="Minimum CGPA required")
    skills_required = models.TextField()
    backlog_allowed = models.CharField(max_length = 20, choices = BACKLOG_CHOICES)
    batch_eligible = models.CharField(max_length=50, choices =YEAR_CHOICES)

    selection_process = models.TextField(help_text="Stages like Aptitude Test, Coding Test, Interviews")
    application_deadline = models.DateField()
    drive_date = models.DateField()
    applied = models.BooleanField(default=False)
    applied_students = models.ManyToManyField('StudentProfile', related_name='applied_drives', blank=True)
    selected_students = models.ManyToManyField('StudentProfile', related_name="selected_drives", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.company.name} - {self.job_role} ({self.drive_date})"

    def is_expired(self):
        return self.application_deadline < now().date()

    def status(self):
        return "Expired" if self.is_expired() else "Active"    




class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")

    # Personal Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    # Professional Details
    enrollment_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    year_of_study = models.IntegerField(null=True, blank=True)
    current_semester = models.IntegerField()
    
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(help_text="Enter skills separated by commas")
    certifications = models.FileField(upload_to='certifications/', blank=True, null=True)

    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.enrollment_number}"
