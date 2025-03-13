from django.urls import path 
from home import views 

urlpatterns = [
    # Company URLs
    path("",views.home,name ="home"),
    path("companies/", views.company_list, name="company_list"),
    path("company_dashboard/", views.company_dashboard, name="company_dashboard"),
    path("company/<int:pk>/", views.company_detail, name="company_detail"),
    path("company/add/", views.company_create, name="company_create"),
    path("company/edit/<int:pk>/", views.company_update, name="company_update"),
    path("company/delete/<int:pk>/", views.company_delete, name="company_delete"),

    # Drive URLs
    path("drives/", views.drive_list, name="drive_list"),
    path("drive/<int:pk>/", views.drive_detail, name="drive_detail"),
    path("drive/add/", views.drive_create, name="drive_create"),
    path("drive/edit/<int:pk>/", views.drive_update, name="drive_update"),
    path("drive/delete/<int:pk>/", views.drive_delete, name="drive_delete"),
    path("drive/apply_drive/<int:pk>/", views.apply_drive, name="apply_drive"),
    path("drive/<int:pk>/applied-students/", views.applied_students, name="applied_students"),
    path("drive/<int:pk>/selected-students/", views.selected_students, name="selected_students"),
    path("drive/<int:drive_id>/select-student/<int:student_id>/", views.select_student, name="select_student"),

    
    #student URLs
    path("student/create", views.create_student_profile, name="create_student_profile"),
    path("student/update", views.student_profile_update, name="student_profile_update"),
    path("student/dashboard", views.student_dashboard, name="student_dashboard"),
    path('student/dashboard/<int:student_id>/', views.student_dashboard, name='student_dashboard_admin'), 
    path("student/active_drives", views.active_drives, name="active_drives"),
    path("student/student_list", views.student_list, name="student_list"),
    path("admins/admin_dashboard", views.admin_dashboard, name="admin_dashboard"),



]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
