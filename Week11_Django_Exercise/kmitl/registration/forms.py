from django import forms
from django.forms import ModelForm, FileInput
from django.core.exceptions import ValidationError
from .models import Faculty, Section, Student, StudentProfile, Course

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
            "address",
            "image"
        ]
        widgets = {
            "image": FileInput(attrs={"class": "sr-only"})
        }

    def clean_email(self):
        cleaned_data = self.clean()
        email = cleaned_data.get("email")
        if not email.endswith("@kmitl.ac.th"):
            return False
            # raise ValidationError("Email must end with @kmitl.ac.th")
        
        return email
    
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = "__all__"
        exclude = ["course"]
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    

    def clean(self):
        clean_data = super().clean()
        start_time = clean_data.get("start_time")
        end_time = clean_data.get("end_time")
        capacity = clean_data.get("capacity")

        if start_time and end_time and end_time < start_time:
            self.add_error("end_time", "End time must be after start time")
        if capacity is not None and capacity <= 20:
            self.add_error("capacity", "Capacity must be over 20")
        return clean_data