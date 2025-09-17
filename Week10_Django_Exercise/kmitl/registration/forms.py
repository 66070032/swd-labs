from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Faculty, Section, Student, StudentProfile

""" class StudentForm(forms.Form):
    student_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    faculty = forms.ModelChoiceField(
        queryset = Faculty.objects.all(),
        # widget=forms.RadioSelect,
        empty_label = "Select an option",
        required = False
    )
    enrolled_sections = forms.ModelMultipleChoiceField(
        queryset = Section.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False
    )
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea) """

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "faculty",
            "enrolled_sections"
        ]
    
    def clean_student_id(self):
        cleaned_data = self.clean()
        student_id = cleaned_data.get("student_id")

        qs = Student.objects.filter(student_id=student_id)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # << ข้าม record เดิม
        if qs.exists():
            raise ValidationError("Student ID already exists.")
        
        return student_id

class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "email",
            "phone_number",
            "address"
        ]

    def clean_email(self):
        cleaned_data = self.clean()
        email = cleaned_data.get("email")
        if not email.endswith("@kmitl.ac.th"):
            raise ValidationError("Email must end with @kmitl.ac.th")
        
        return email