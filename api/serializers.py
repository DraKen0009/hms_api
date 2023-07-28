from rest_framework import serializers

from .models import User, Department, PatientReport


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'department']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializerModified(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'department']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },

        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'specialization', 'diagnostics', 'location']


class PatientReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientReport
        fields = ['record_id', 'patient', 'department', 'created', 'diagnostics', 'observations', 'treatments']
        extra_kwargs = {
            'created': {
                'read_only': True,
            },

        }

    def to_representation(self, instance):
        rep = super(PatientReportSerializer, self).to_representation(instance)
        rep['patient'] = instance.patient.username
        rep['department'] = instance.department.name
        return rep

    def validate(self, attrs):
        print(attrs)
        patient = attrs.get('patient')
        if patient.role != User.Role.PATIENT:
            raise serializers.ValidationError("Report can be created for patients only")
        return attrs
