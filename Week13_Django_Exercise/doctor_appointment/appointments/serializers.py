from rest_framework import serializers
from appointments.models import Doctor, Patient, Appointment

from django.utils import timezone
import datetime

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email"
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address"
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    # ใช้ id ตรง ๆ โดยไม่ต้องมี _id
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), write_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)

    # ส่ง nested object กลับเมื่อ GET
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)
    patient_detail = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",          # ใช้รับ id ตอน POST
            "doctor_detail",   # แสดง nested ตอน GET
            "patient",
            "patient_detail",
            "date",
            "at_time",
            "details"
        ]

    def update(self, instance, validated_data):
        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.patient = validated_data.get('patient', instance.patient)
        instance.date = validated_data.get('date', instance.date)
        instance.at_time = validated_data.get('at_time', instance.at_time)
        instance.details = validated_data.get('details', instance.details)
        instance.save()
        return instance

    def validate(self, data):
        today = timezone.localdate()
        now = timezone.localtime()
        current_time = now.time()

        appointment_date = data.get("date")
        appointment_time = data.get("at_time")

        if appointment_date < today:
            raise serializers.ValidationError("Appointment date must not be in the past.")

        if appointment_date == today and appointment_time <= current_time:
            raise serializers.ValidationError("Appointment time must be in the future.")

        return data