from django import forms
from .models import Company, Drive,StudentProfile

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'industry_type', 'website', 'contact_person','contact_email','contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter company name'}),
            'location': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Location'}),
            'industry_type': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control','placeholder': 'https://xyz.com'}),
            'contact_person':forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter contact person name'}),
            'contact_email':forms.EmailInput(attrs={'class':'form-control','placeholder': 'Enter contact persons email'}),
            'contact_phone':forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter contact persons phone'})
        }

class DriveForm(forms.ModelForm):
    class Meta:
        model = Drive
        fields = [
            'company', 'job_role', 'job_description', 'salary_package',
            'employment_type', 'bond_period', 'job_location', 'cgpa_requirement','skills_required','backlog_allowed','batch_eligible','selection_process','application_deadline','drive_date'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'job_role': forms.TextInput(attrs={'class': 'form-control' ,'placeholder': 'Enter job role'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Describe the job role', 'rows': 3}),
            'salary_package': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter salary in LPA'}),
            'employment_type': forms.Select(attrs={'class': 'form-control',}),
            'bond_period': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'In years'}),
            'job_location': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Describe selection process'}),
            'cgpa_requirement': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Minimum CGPA required'}),
            'skills_required': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter required skills'}),
            'backlog_allowed': forms.Select(attrs={'class': 'form-control'}),
            'batch_eligible': forms.Select(attrs={'class': 'form-control'}),
            'selection_process': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Describe selection process'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
            'drive_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'phone_number',
            'address', 'city', 'state', 'country', 'zip_code',
            'enrollment_number', 'branch', 'year_of_study', 'current_semester',
            'resume', 'skills', 'certifications', 'cgpa',
            'linkedin_profile', 'github_profile'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter your full address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'enrollment_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enrollement number'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'year_of_study': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, SQL'}),
            'certifications': forms.FileInput(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn Profile URL'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Profile URL'}),
        }
