from django.urls import path

from . import views

urlpatterns = [
    path("students/", views.student_list, name="student_list"),
    path("professor/", views.professor_list, name="professor_list"),
    path("course/", views.course_list, name="course_list"),
    path("faculty/", views.faculty_list, name="faculty_list"),
    path("create_student/", views.create_student, name="create_student"),

    path("update_student/<int:student_id>", views.update_student, name="update_student")
]