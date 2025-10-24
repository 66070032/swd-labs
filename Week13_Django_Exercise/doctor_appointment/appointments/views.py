from django.shortcuts import render
from appointments.models import Doctor, Patient, Appointment
from appointments.serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

# Create your views here.
class DoctorList(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class PatientList(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class AppointmentList(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AppointmentDetail(APIView):
    def get(self, request, pk):
        try:
            apppointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return HttpResponse(status=404)
        serializer = AppointmentSerializer(apppointment)
        return JsonResponse(serializer.data)
    
    def put(self, request, pk):
        try:
            apppointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return HttpResponse(status=404)
        data = JSONParser().parse(request)
        serializer = AppointmentSerializer(apppointment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    def delete(self, request, pk):
        try:
            apppointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return HttpResponse(status=404)
        apppointment.delete()
        return HttpResponse(status=204)