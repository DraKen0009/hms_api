from django.contrib import admin

from api.models import User, Department,PatientReport

# Register your models here.

admin.site.register(User)
admin.site.register(Department)
admin.site.register(PatientReport)
