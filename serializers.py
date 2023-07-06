from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Consultation, HospitalSection, Doctor, Patient, Reservation
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.password_validation import validate_password as validate_pass
from django.contrib.auth.hashers import make_password


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "id",
            "section",
            "doctor_name",
            "doctor_description",
            "doctor_price",
            "from_time",
            "to_time",
            "Work_day",
            "description",
            "session_price",
        )


class HospitalSectionSerializer(ModelSerializer):
    class Meta:
        model = HospitalSection
        fields = ("id", "name")


class HospitalSerializer(ModelSerializer):
    class Meta:
        model = HospitalSection
        fields = ("id", "name")


class UserRegisterSerializer(ModelSerializer):
    access = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ("first_name", "phone", "gender", "email", "password", "access")
        extra_kwargs = {"password": {"write_only": True}}

    def get_access(self, user):
        return str(AccessToken.for_user(user))

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def validate_password(self, value):
        validate_pass(value)
        return value

    def save(self, **kwargs):
        return super().save(
            **kwargs,
            username=self.validated_data["email"],
            password=make_password(self.validated_data["password"]),
        )


class DoctorDetailsSerializer(serializers.ModelSerializer):
    section = HospitalSectionSerializer(read_only=True)
    hospital = HospitalSerializer(source="section.hospital", read_only=True)
    email = serializers.CharField(source="user.email", required=False)

    class Meta:
        model = Doctor
        fields = (
            "email",
            "doctor_name",
            "doctor_description",
            "doctor_address",
            "waiting_time",
            "doctor_price",
            "from_time",
            "to_time",
            "Work_day",
            "section",
            "hospital",
            "description",
            "session_price",
        )

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {"email": instance.user.email})
        instance = super().update(instance, validated_data)
        instance.user.email = user_data["email"]
        instance.user.save()
        return instance


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("first_name", "phone", "gender", "email")


class ReservationsSerializer(serializers.ModelSerializer):
    doctor_details = DoctorDetailsSerializer(read_only=True, source="doctor")
    patient = PatientSerializer(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Doctor.objects.all()
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "date",
            "doctor",
            "patient",
            "doctor_details",
            "created_at",
        )
        extra_kwargs = {"created_at": {"read_only": True}}


class ConsultationSerializer(serializers.ModelSerializer):
    section_details = HospitalSectionSerializer(read_only=True, source="section")

    class Meta:
        model = Consultation
        fields = "__all__"
        extra_kwargs = {"patient": {"read_only": True}}
