from django.shortcuts import render, redirect

from registration.models import *
from django.db.models import Count, Q, F, Value
from django.db.models.functions import Concat
from registration.forms import StudentForm

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
        # bind data to form
        form = StudentForm(request.POST)
        # validate data in the form
        if form.is_valid():
            # access cleaned_data
            student_id = form.cleaned_data["student_id"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            faculty = form.cleaned_data["faculty"]
            enrolled_sections = form.cleaned_data["enrolled_sections"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            address = form.cleaned_data["address"]

            print("student_id", student_id)
            print("first_name", first_name)
            print("last_name", last_name)
            print("faculty", faculty)
            print("enrolled_sections", enrolled_sections)
            print("email", email)
            print("phone_number", phone_number)
            print("address", address)

            # Assume that this view send email
            # recipients = ["info@example.com"]
            # if cc_myself:
            #     recipients.append(sender)

            # send_mail(subject, message, sender, recipients)

            # redirect to "thanks" page when the email has been sent
            return redirect("student_list")
    else:
        form = StudentForm()
    
    return render(request, "create_student.html", {"form": form})

def create(request):
    student_id1 = request.POST.get("student_id")
    faculty1 = request.POST.get("faculty")
    fn1 = request.POST.get("first_name")
    ln1 = request.POST.get("last_name")
    email1 = request.POST.get("email")
    phone1 = request.POST.get("phone_number")
    address1 = request.POST.get("address")
    sections1 = request.POST.getlist("enrolled_sections")

    fac = Faculty.objects.get(id = faculty1)
    st1 = Student.objects.create(student_id = student_id1,first_name = fn1,last_name = ln1,faculty=fac)
    stp1 = StudentProfile.objects.create(student =st1,email = email1,phone_number = phone1,address = address1)
    
    for i in sections1:
        sec = Section.objects.get(id = i)
        st1.enrolled_sections.add(sec)
    return redirect("/registration/students")

def update_student(request, student_id):

    student = Student.objects.get(student_id=student_id)
    profile = StudentProfile.objects.get(student=student)

    data = {
        "student_id": student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "faculty": student.faculty,
        "enrolled_sections": student.enrolled_sections.all(),
        "email": profile.email,
        "phone_number": profile.phone_number,
        "address": profile.address
    }

    
    if request.method == "POST":
        # bind data to form
        form = StudentForm(request.POST)
        # validate data in the form
        if form.is_valid():
            # access cleaned_data
            student.student_id = form.cleaned_data["student_id"]
            student.first_name = form.cleaned_data["first_name"]
            student.last_name = form.cleaned_data["last_name"]
            student.faculty = form.cleaned_data["faculty"]
            student.enrolled_sections.set(form.cleaned_data["enrolled_sections"])
            profile.email = form.cleaned_data["email"]
            profile.phone_number = form.cleaned_data["phone_number"]
            profile.address = form.cleaned_data["address"]

            student.save()
            profile.save()

            # Assume that this view send email
            # recipients = ["info@example.com"]
            # if cc_myself:
            #     recipients.append(sender)

            # send_mail(subject, message, sender, recipients)

            # redirect to "thanks" page when the email has been sent
            return redirect("student_list")
    else:
        form = StudentForm(initial=data)

    return render(request, "update_student.html", {"form": form, "student_id": student_id})