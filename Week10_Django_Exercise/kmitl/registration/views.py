from django.shortcuts import render, redirect

from registration.models import *
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Concat
from registration.forms import StudentForm, StudentProfileForm, CourseForm, SectionForm

# Create your views here.
def student_list(request):
    search = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    student_list = Student.objects.all()

    if search:
        if filter_type == "email":
            student_list = Student.objects.filter(studentprofile__email__icontains = search)
        elif filter_type == "faculty":
            student_list = Student.objects.filter(faculty__name__icontains = search)
        else:
            student_list = Student.objects.annotate(
                full_name = Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains = search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )
    return render(request, 'index.html', context={
        'search': search,
        'filter': filter_type,
        'student_list': student_list,
        'total': student_list.count()
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
        'professor_list': professor_list,
        'search': search,
        'filter': filter_type
    })


def faculty_list(request):
    search = request.GET.get("search", "").strip()
    faculty_list = Faculty.objects.annotate(professor_count = Count("professor", distinct=True), student_count = Count("student", distinct=True)).all()
    
    if search:
        faculty_list = Faculty.objects.annotate(professor_count = Count("professor", distinct=True), student_count = Count("student", distinct=True)).filter(name__icontains = search).all()
    return render(request, "faculty.html", context={
        "faculty_list": faculty_list,
        "total": faculty_list.count(),
        "search": search
    })

def course_list(request):
    search = request.GET.get("search", "").strip()
    course_list = Course.objects.all()
    
    if search:
        course_list = Course.objects.filter(course_name__icontains = search).all()
    return render(request, "course.html", context={
        "course_list": course_list,
        "total": course_list.count(),
        "search": search
    })

def create_student(request):
    if request.method == "POST":
        s_form = StudentForm(request.POST)
        p_form = StudentProfileForm(request.POST)
        if s_form.is_valid() and p_form.is_valid():
            student = s_form.save()
            profile = p_form.save(commit=False)
            profile.student = student
            profile.save()
            
            return redirect("student_list")
    else:
        s_form = StudentForm()
        p_form = StudentProfileForm()
    
    return render(request, "create_student.html", {"s_form": s_form, "p_form": p_form})

def update_student(request, student_id):

    student = Student.objects.get(student_id=student_id)
    profile = StudentProfile.objects.get(student=student)

    if request.method == "POST":
        s_form = StudentForm(request.POST, instance=student)
        p_form = StudentProfileForm(request.POST, instance=profile)

        if s_form.is_valid() and p_form.is_valid():
            print("POST:", request.POST)
            print("s_form.cleaned_data:", s_form.cleaned_data)
            print("s_form.changed_data:", s_form.changed_data)

            student = s_form.save(commit=False)
            profile =  p_form.save(commit=False)
            profile.student = student
            profile.save()
            student.save()
            s_form.save_m2m()          # ถ้ามี M2M ต้องเรียก ไม่งั้นไม่เซฟ

            return redirect("student_list")
    else:
        s_form = StudentForm(instance=student)
        p_form = StudentProfileForm(instance=profile)

    return render(request, "update_student.html", {"s_form": s_form, "p_form": p_form, "student_id": student_id})

def create_course(request):
    if request.method == "POST":
        c_form = CourseForm(request.POST)
        s_form = SectionForm(request.POST)
        if c_form.is_valid() and s_form.is_valid():
            course = c_form.save()
            section = s_form.save(commit=False)
            section.course = course
            section.save()
            return redirect('course_list')
    else:
        # method get
        c_form = CourseForm()
        s_form = SectionForm()
    return render(request, "create_course.html", { "cform": c_form, "sform": s_form })

def update_course(request, course_code):
    crs = Course.objects.get(course_code = course_code)
    sec = Section.objects.filter(course = crs).first()
    
    if request.method == "POST":
        course_form = CourseForm(request.POST, instance=crs)
        section_form = SectionForm(request.POST, instance=sec)
        if course_form.is_valid() and section_form.is_valid():
            course = course_form.save()
            section = section_form.save(commit=False)
            section.course = course
            section.save()
            return redirect('course_list')
        else:
            print(course_form.errors)
            print(section_form.errors)
    else:
        course_form = CourseForm(instance=crs)
        section_form = SectionForm(instance=sec)
    return render(request, "update_course.html", {
        "cform": course_form,
        "sform": section_form,
        "course": crs
    })