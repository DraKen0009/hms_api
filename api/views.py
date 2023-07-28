# Create your views here.
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, Department, PatientReport
from api.permissions import DoctorOnly, PatientSpecific, DoctorsPatientSpecific, DepartmentPatient, \
    DepartmentDoctor, DoctorSpecific
from api.serializers import UserSerializer, UserSerializerModified, DepartmentSerializer, PatientReportSerializer


def home(request):
    return render(request,'api/landing.html')
class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'msg': "logged in",
            "data": serializer.data
        })


class DoctorListView(ListCreateAPIView):
    queryset = User.doctors.all()
    serializer_class = UserSerializerModified
    permission_classes = [DoctorOnly]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)


class PatientListView(ListCreateAPIView):
    queryset = User.patients.all()
    serializer_class = UserSerializerModified
    permission_classes = [DoctorOnly]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)


class DoctorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.doctors.all()
    serializer_class = UserSerializer
    permission_classes = [DoctorSpecific]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)


class PatientDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.patients.all()
    serializer_class = UserSerializer
    permission_classes = [PatientSpecific]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)


class DepartmentListView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DoctorOnly]

class DepartmentDoctorView(ListCreateAPIView):
    serializer_class = UserSerializerModified
    permission_classes = [DepartmentDoctor]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)

    def get_queryset(self, **kwargs):
        id = self.kwargs['pk']
        dep = Department.objects.filter(id=id).first()
        if dep is None:
            return None
        queryset = dep.user_set.filter(role=User.Role.DOCTOR)
        return queryset


class DepartmentPatientView(ListCreateAPIView):
    serializer_class = UserSerializerModified
    permission_classes = [DepartmentPatient]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)

    def get_queryset(self, **kwargs):
        id = self.kwargs['pk']
        dep = Department.objects.filter(id=id).first()
        if dep is None:
            return None
        queryset = dep.user_set.filter(role=User.Role.PATIENT)
        return queryset


class PatientReportListView(ListCreateAPIView):
    serializer_class = PatientReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, **kwargs):
        qs = PatientReport.objects.all().filter(student__role=User.Role.PATIENT)
        return qs


class PatientReportDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientReportSerializer
    permission_classes = [DoctorsPatientSpecific]

    def get_queryset(self, **kwargs):
        qs = PatientReport.objects.all().filter(student__role=User.Role.PATIENT)
        return qs
