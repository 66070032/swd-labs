from django.shortcuts import render
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponse as HTTPResponse
import datetime
from .models import *
from django.shortcuts import redirect

# Create your views here.
def student_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    student_list = Student.objects.all()

    if search:
        if filter_type == "email":
            student_list = Student.objects.filter(studentprofile__email__icontains=search)
        elif filter_type == "faculty":
            student_list = Student.objects.filter(faculty__name__icontains=search)
        else:
            student_list = Student.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )

    return render(request, 'index.html', context={
        'total': student_list.count(),
        'search': search,
        'filter': filter_type,
        'student_list': student_list
    })

def professor_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    professor_list = Professor.objects.all()

    if search:
        if filter_type == "faculty":
            professor_list = Professor.objects.filter(faculty__name__icontains=search)
        else:
            professor_list = Professor.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )

    return render(request, 'professor.html', context={
        'total': professor_list.count(),
        'search': search,
        'filter': filter_type,
        'professor_list': professor_list
    })

def course_list(request):
    search = request.GET.get("search", "").strip()
    course_list = Course.objects.all()

    if search:
        course_list = course_list.filter(
            Q(course_code__icontains=search) | Q(course_name__icontains=search)
        )
    return render(request, 'course.html', context={
        'total': course_list.count(),
        'search': search,
        'course_list': course_list
    })

def faculty_list(request):
    search = request.GET.get("search", "").strip()
    faculty_list = Faculty.objects.all()

    if search:
        faculty_list = faculty_list.filter(name__icontains=search)

    faculty_list = faculty_list.annotate(
        professor_count=Count("professor", distinct=True),
        student_count=Count("student", distinct=True)
    ).order_by("id")

    return render(request, 'faculty.html', context={
        'total': faculty_list.count(),
        'search': search,
        'faculty_list': faculty_list
    })

def create_student(request):
    faculties = Faculty.objects.all()
    section = Section.objects.all()
    
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        faculty_id = request.POST.get("faculty")
        sections = request.POST.getlist("section_ids")

        faculty = Faculty.objects.get(id=faculty_id)
        student = Student.objects.create(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            faculty=faculty
        )
        studentProfile = StudentProfile.objects.create(
            student=student,
            email=email,
            phone_number=phone_number,
            address=address
        )
        for i in sections:
            sec = Section.objects.get(id = i)
            student.enrolled_sections.add(sec)

        return redirect("/")

    # Render the create student form
    return render(request, 'create_student.html', context={
        'faculties': faculties,
        'sections': section
    })