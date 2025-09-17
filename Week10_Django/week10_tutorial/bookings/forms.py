from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError

from bookings.models import Booking

class BookingForm(ModelForm):
    start_time = SplitDateTimeField(widget=SplitDateTimeWidget(
                date_attrs={"class": "input", "type": "date"},
                time_attrs={"class": "input", "type": "time"}
            ))
    end_time = SplitDateTimeField(widget=SplitDateTimeWidget(
                date_attrs={"class": "input", "type": "date"},
                time_attrs={"class": "input", "type": "time"}
            ))

    class Meta:
        model = Booking
        fields = [
            "room", 
            "staff", 
            "email", 
            "start_time", 
            "end_time", 
            "purpose"
        ]
        widgets = {
            "email": TextInput(attrs={"class": "input"}),
            "purpose": Textarea(attrs={"rows": 5, "class": "textarea"})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time < start_time:
            raise ValidationError(
                    "End time cannot be before start time"
                )
        bookings = Booking.objects.filter(
            start_time__lte=end_time, 
            end_time__gte=start_time, 
            room=room
        )
        if bookings.count() > 0:
            raise ValidationError(
                    "This room has already been booked for the selected time"
                )

        return cleaned_data