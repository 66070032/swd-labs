from django.urls import path

from bookings import views

urlpatterns = [
    path("", views.BookingList.as_view(), name="booking-list"),
    path("create/", views.BookingCreate.as_view(), name="booking-create"),
    path("<int:booking_id>", views.BookingDelete.as_view(), name="booking-delete"),
]