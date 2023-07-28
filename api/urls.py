from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from api.views import RegisterView, DepartmentPatientView, DepartmentDoctorView, DepartmentDetailView, \
    DoctorDetailView, DepartmentListView, DoctorListView, PatientReportDetailView, PatientListView, \
    PatientReportListView, PatientDetailView

urlpatterns = [

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('doctors/', DoctorListView.as_view()),
    path('doctors/<int:pk>/', DoctorDetailView.as_view()),
    path('patients/<int:pk>/', PatientDetailView.as_view()),
    path('patients/', PatientListView.as_view()),
    path('departments/', DepartmentListView.as_view()),
    path('departments/<int:pk>/', DepartmentDetailView.as_view()),
    path('department/<int:pk>/teachers/', DepartmentDoctorView.as_view()),
    path('department/<int:pk>/students/', DepartmentPatientView.as_view()),
    path('patient_record/', PatientReportListView.as_view()),
    path('patient_record/<int:pk>/', PatientReportDetailView.as_view()),

]
