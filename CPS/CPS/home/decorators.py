from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect,render
from functools import wraps

def student_required(view_func):
    """
    Custom decorator to allow only students to access a view.
    Redirects unauthorized users.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page

        # Check if the user is in the "Students" group
        if request.user.groups.filter(name="Students").exists():
            return view_func(request, *args, **kwargs)

        # If the user is not a student, deny access
        return render(request,'no_permission.html')  # Returns 403 Forbidden
        
    return _wrapped_view



def superuser_required(view_func):
    """
    Custom decorator to allow only superusers to access a view.
    Redirects unauthorized users.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page

        # Check if the user is a superuser
        if request.user.is_superuser or request.user.groups.filter(name="Companies").exists() :
            return view_func(request, *args, **kwargs)

        # If the user is not a superuser, deny access
        return render(request,'no_permission.html')  # Returns 403 Forbidden
        
    return _wrapped_view