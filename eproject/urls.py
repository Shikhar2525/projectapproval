from django.urls import path
from . import views
urlpatterns = [
   path("studentlogin", views.studentlogin, name="studentlogin"),
   path("facultylogin", views.facultylogin, name="facultylogin"),
   path("studentsignup", views.studentsignup, name="studnetsignup"),
   path("facultysignup", views.facultysignup, name="facultysignup"),
   path("studsignup", views.handlestudentsignup, name="handlestudentsignup"),
   path("studlogin", views.handlestudentlogin, name="handlestudentlogin"),
   path("studlogout", views.studlogout, name="studlogout"),
   path("addteam", views.addteam, name="addteam"),
   path("changepp", views.changepp, name="changepp"),
   path("upload", views.upload, name="upload"),
   path("handleproject", views.handleproject, name="handleproject"),
   path("view_project", views.view_project, name="view_project"),
   path("error", views.error, name="error"),
   path("add_comment", views.add_comment, name="add_comment"),
   path("delete_project", views.delete_project, name="delete_project"),
   path("select_cat", views.select_cat, name="select_cat"),


  # path("member_added", views.member_added, name="member_added"),
]
