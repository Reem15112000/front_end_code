from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from main.permissions import IsDoctor, IsPatientOrReadOnly

from .models import Doctor, Hospital, HospitalSection, Patient, Consultation, Reservation
from .serializers import (
    ConsultationSerializer,
    DoctorDetailsSerializer,
    DoctorSerializer,
    HospitalSectionSerializer,
    HospitalSerializer,
    ReservationsSerializer,
    UserRegisterSerializer,
)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


class HospitalSectionListAPIView(ListAPIView):
    serializer_class = HospitalSectionSerializer
    queryset = HospitalSection.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("hospital__id",)


class DoctorListAPIView(ListAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("section__id", "section__hospital__id")


class HospitalListAPIView(ListAPIView):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("type",)


class UserRegisterView(CreateAPIView):
    permission_classes = ()
    serializer_class = UserRegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.validated_data["role"] = (
            "doctor" if hasattr(serializer.user, "doctor_profile") else "patient"
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class DoctorDetailsView(RetrieveUpdateAPIView):
    serializer_class = DoctorDetailsSerializer
    permission_classes = (IsAuthenticated, IsDoctor)

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


class MyReservationsView(ListCreateAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = (IsAuthenticated, IsPatientOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return user.doctor_profile.reservations.all()
        elif hasattr(user, "patient"):
            return user.patient.reservations.all()
        return []

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient)


class MyConsultationsView(ListCreateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = (IsAuthenticated, IsPatientOrReadOnly)
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return user.doctor_profile.section.consultations.all()
        elif hasattr(user, "patient"):
            return user.patient.consultations.all()
        return []
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient)
    

class ReplyToConsultationView(RetrieveUpdateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = (IsAuthenticated, IsDoctor)
    http_method_names = ["patch", "get"]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor_profile"):
            return user.doctor_profile.section.consultations.all()
        return []

    def perform_update(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)


def index(request):
    return render(request, 'pages/index.html')

@permission_required('admin')
def addDep(request):
    addHos = Hospital.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        hospital = request.POST.get('hospital')
        dep = HospitalSection(name = name, hospital = Hospital.objects.get(name = hospital))
        dep.save()
        return redirect('mainAdmin')
    return render(request, 'pages/addDep.html', {'addHos':addHos})

@permission_required('admin')
def addDoc(request):
    addDep = HospitalSection.objects.all()
    doctor = User.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        docDescription = request.POST.get('docDescription')
        docAddress = request.POST.get('docAddress')
        wait = request.POST.get('wait')
        salary = request.POST.get('salary')
        start = request.POST.get('start')
        end = request.POST.get('end')
        days = request.POST.get('days')
        price = request.POST.get('price')
        dep = request.POST.get('dep')
        description = request.POST.get('description')
        docAccount = request.POST.get('docAccount')
        doctor = Doctor(doctor_name = name, doctor_description = docDescription, doctor_address = docAddress, waiting_time = wait, doctor_price = salary, from_time = start, to_time = end, Work_day = days, session_price = price, description = description, user = User.objects.get(email = docAccount), section = HospitalSection.objects.get(name = dep))
        doctor.save()
        return redirect('mainAdmin')
    return render(request, 'pages/addDoc.html', {'addDep':addDep, 'doctor':doctor})

@permission_required('admin')
def addHos(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        typeHos = request.POST.get('typeHos')
        hospital = Hospital(name = name, type = typeHos)
        hospital.save()
        return redirect('mainAdmin')
    return render(request, 'pages/addHos.html')

@login_required
def hospital1Dep1(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital1Dep1.html', {'doctor':doctor})

@login_required
def hospital1Dep1Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'النساء و التوليد'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'زينب الششتاوى'))
        consutltation.save()
        return redirect('hospital1Dep1Doc1Consultation')
    return render(request, 'pages/hospital1Dep1Doc1Consultation.html', {'patient':patient})

@login_required
def hospital1Dep1Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep1Doc1Reservation')
    return render(request, 'pages/hospital1Dep1Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital1Dep1Doc2Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'النساء و التوليد'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'مى بسيونى'))
        consutltation.save()
        return redirect('hospital1Dep1Doc2Consultation')
    return render(request, 'pages/hospital1Dep1Doc2Consultation.html', {'patient':patient})

@login_required
def hospital1Dep1Doc2Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep1Doc2Reservation')
    return render(request, 'pages/hospital1Dep1Doc2Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital1Dep1Doc3Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'النساء و التوليد'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'عاطف نبيل'))
        consutltation.save()
        return redirect('hospital1Dep1Doc3Consultation')
    return render(request, 'pages/hospital1Dep1Doc3Consultation.html', {'patient':patient})

@login_required
def hospital1Dep1Doc3Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep1Doc3Reservation')
    return render(request, 'pages/hospital1Dep1Doc3Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital1Dep2(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital1Dep2.html', {'doctor':doctor})

@login_required
def hospital1Dep2Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'العناية'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'محمد جبريل'))
        consutltation.save()
        return redirect('hospital1Dep2Doc1Consultation')
    return render(request, 'pages/hospital1Dep2Doc1Consultation.html', {'patient':patient})

@login_required
def hospital1Dep2Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep2Doc1Reservation')
    return render(request, 'pages/hospital1Dep2Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital1Dep2Doc2Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'العناية'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'جمال الخلال'))
        consutltation.save()
        return redirect('hospital1Dep2Doc2Consultation')
    return render(request, 'pages/hospital1Dep2Doc2Consultation.html', {'patient':patient})

@login_required
def hospital1Dep2Doc2Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep2Doc2Reservation')
    return render(request, 'pages/hospital1Dep2Doc2Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital1Dep3(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital1Dep3.html', {'doctor':doctor})

@login_required
def hospital1Dep3Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'الأطفال'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'إيمان ابو خشبة'))
        consutltation.save()
        return redirect('hospital1Dep3Doc1Consultation')
    return render(request, 'pages/hospital1Dep3Doc1Consultation.html', {'patient':patient})

@login_required
def hospital1Dep3Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep3Doc1Reservation')
    return render(request, 'pages/hospital1Dep3Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital1Dep3Doc2Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'الأطفال'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'أسماء بدر الدين'))
        consutltation.save()
        return redirect('hospital1Dep3Doc2Consultation')
    return render(request, 'pages/hospital1Dep3Doc2Consultation.html', {'patient':patient})

@login_required
def hospital1Dep3Doc2Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital1Dep3Doc2Reservation')
    return render(request, 'pages/hospital1Dep3Doc2Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep1(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital2Dep1.html', {'doctor':doctor})

@login_required
def hospital2Dep1Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'النفسية'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'عاطف عبد السميع'))
        consutltation.save()
        return redirect('hospital2Dep1Doc1Consultation')
    return render(request, 'pages/hospital2Dep1Doc1Consultation.html', {'patient':patient})

@login_required
def hospital2Dep1Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep1Doc1Reservation')
    return render(request, 'pages/hospital2Dep1Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep1Doc2Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'النفسية'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'مروة السيرى'))
        consutltation.save()
        return redirect('hospital2Dep1Doc2Consultation')
    return render(request, 'pages/hospital2Dep1Doc2Consultation.html', {'patient':patient})

@login_required
def hospital2Dep1Doc2Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep1Doc2Reservation')
    return render(request, 'pages/hospital2Dep1Doc2Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep1Doc3Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'النفسية'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'مصطفى عبد القادر'))
        consutltation.save()
        return redirect('hospital2Dep1Doc3Consultation')
    return render(request, 'pages/hospital2Dep1Doc3Consultation.html', {'patient':patient})

@login_required
def hospital2Dep1Doc3Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep1Doc3Reservation')
    return render(request, 'pages/hospital2Dep1Doc3Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep2(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital2Dep2.html', {'doctor':doctor})

@login_required
def hospital2Dep2Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'امراض الدم'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'امل عفيفى'))
        consutltation.save()
        return redirect('hospital2Dep2Doc1Consultation')
    return render(request, 'pages/hospital2Dep2Doc1Consultation.html', {'patient':patient})

@login_required
def hospital2Dep2Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep2Doc1Reservation')
    return render(request, 'pages/hospital2Dep2Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep3(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital2Dep3.html', {'doctor':doctor})

@login_required
def hospital2Dep3Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'الجراحة العامة'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'عمرو كامل'))
        consutltation.save()
        return redirect('hospital2Dep3Doc1Consultation')
    return render(request, 'pages/hospital2Dep3Doc1Consultation.html', {'patient':patient})

@login_required
def hospital2Dep3Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep3Doc1Reservation')
    return render(request, 'pages/hospital2Dep3Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep4(request):
    doctor = Doctor.objects.all()
    return render(request, 'pages/hospital2Dep4.html', {'doctor':doctor})

@login_required
def hospital2Dep4Doc1Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'العظام'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'شريف مصطفى'))
        consutltation.save()
        return redirect('hospital2Dep4Doc1Consultation')
    return render(request, 'pages/hospital2Dep4Doc1Consultation.html', {'patient':patient})

@login_required
def hospital2Dep4Doc1Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep4Doc1Reservation')
    return render(request, 'pages/hospital2Dep4Doc1Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def hospital2Dep4Doc2Consultation(request):
    patient = Patient.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        age = request.POST.get('age')
        type1 = request.POST.get('type1')
        weight = request.POST.get('weight')
        diseases = request.POST.get('diseases')
        description = request.POST.get('description')
        reply = request.POST.get('reply')
        consutltation = Consultation(patient = Patient.objects.get(username = name), section = HospitalSection.objects.get(name = 'العظام'), type = type1, age = age, weight = weight, has_any_disease = diseases, description = description, reply = reply, doctor_replied = Doctor.objects.get(doctor_name = 'هانى الزحلاوى'))
        consutltation.save()
        return redirect('hospital2Dep4Doc2Consultation')
    return render(request, 'pages/hospital2Dep4Doc2Consultation.html', {'patient':patient})

@login_required
def hospital2Dep4Doc2Reservation(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    if request.method == 'POST':
        name =  request.POST.get('name')
        docName = request.POST.get('docName')
        reservation = Reservation(patient = Patient.objects.get(username = name), doctor = Doctor.objects.get(doctor_name = docName))
        reservation.save()
        return redirect('hospital2Dep4Doc2Reservation')
    return render(request, 'pages/hospital2Dep4Doc2Reservation.html', {'patient':patient, 'doctor':doctor})

@login_required
def mainHos1(request):
    section = HospitalSection.objects.all()
    return render(request, 'pages/mainHos1.html', {'section':section, 'hos1':'مستشفى الأمومة'})

@login_required
def mainHos2(request):
    section = HospitalSection.objects.all()
    return render(request, 'pages/mainHos2.html', {'section':section, 'hos2':'مستشفى عين شمس'})

@login_required
def main(request):
    hospital = Hospital.objects.all()
    return render(request, 'pages/main.html', {'hospital':hospital, 'public':'public', 'private':'private'})

@permission_required('admin')
def mainAdmin(request):
    hospital = Hospital.objects.all()
    return render(request, 'pages/main(admin).html', {'hospital':hospital, 'public':'public', 'private':'private'})

@permission_required('admin')
def showConsultation(request):
    consultation = Consultation.objects.all()
    return render(request, 'pages/showConsultation.html', {'consultation':consultation})

@permission_required('admin')
def showReservation(request):
    reservation = Reservation.objects.all()
    return render(request, 'pages/showReservation.html', {'reservation':reservation})

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user=User.objects.create_user(username = email, email = email, password=password)
        new_user.first_name = name
        new_user1 = Patient.objects.create(phone = phone, gender = gender)
        new_user1.first_name = name
        new_user1.username = (name+email)
        new_user.save()
        new_user1.save()
        return redirect('signin')
    return render(request, 'pages/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return  redirect('main')
    return render(request, 'pages/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')