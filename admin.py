from django.contrib import admin

from main.forms import (
    CustomPatientChangeForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    PatientCreationForm,
)
from .models import (
    Consultation,
    HospitalSection,
    Doctor,
    Hospital,
    Patient,
    Reservation,
)
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.unregister([Group, User])
admin.site.register(Reservation)
admin.site.register(Consultation)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
    )
    list_filter = ("type",)


@admin.register(HospitalSection)
class HospitalSectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hospital",
    )
    list_editable = ("hospital",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_name",
        "section",
        "section__hospital",
    )

    def section__hospital(self, obj):
        if obj.section and obj.section.hospital:
            return obj.section.hospital.name

    section__hospital.short_description = "Hospital"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "date_joined",
    )


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    add_form = PatientCreationForm
    form = CustomPatientChangeForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "phone",
                    "gender",
                    "email",
                    "password",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "phone",
                    "gender",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
