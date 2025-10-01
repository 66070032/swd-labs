from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from bookings.models import Booking
from bookings.forms import BookingForm

class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('booking-list')  

        return render(request,'login.html', {"form":form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class BookingList(PermissionRequiredMixin, View):
    permission_required = ["bookings.view_booking"]

    def get(self, request):
        query = request.GET
        bookings = Booking.objects.order_by("start_time")

        if query.get("search"):
            bookings = bookings.filter(
                Q(room__name__icontains=query.get("search")) | 
                Q(staff__name__icontains=query.get("search"))
            )

        return render(request, "booking-list.html", {
            "bookings": bookings
        })


class BookingCreate(PermissionRequiredMixin, View):
    permission_required = ["bookings.add_booking"]

    def get(self, request):
        form = BookingForm()
        return render(request, "booking.html", {
            "form": form,
        })

    def post(self, request):
        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('booking-list')

        return render(request, "booking.html", {
            "form": form
        })

class BookingUpdate(PermissionRequiredMixin, View):
    permission_required = ["bookings.change_booking"]

    def get(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        form = BookingForm(instance=booking)
        return render(request, "booking.html", {
            "form": form,
        })

    def post(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():
            form.save()
            return redirect('booking-list')

        return render(request, "booking.html", {
            "form": form
        })


class BookingDelete(PermissionRequiredMixin, View):
    permission_required = ["bookings.delete_booking"]

    def get(self, request, booking_id):
        booking = Booking.objects.get(pk=booking_id)
        booking.delete()

        return redirect("booking-list")