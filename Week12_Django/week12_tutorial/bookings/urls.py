# bookings/urls.py
from django.urls import path

from bookings import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("", views.BookingList.as_view(), name="booking-list"),
    path("create/", views.BookingCreate.as_view(), name="booking-create"),
    path("update/<int:booking_id>", views.BookingUpdate.as_view(), name="booking-update"),
    path("delete/<int:booking_id>", views.BookingDelete.as_view(), name="booking-delete"),
]