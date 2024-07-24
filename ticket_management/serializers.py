from rest_framework import serializers
from .models import Department, SLA


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def create(self, validated_data):
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.department_name = validated_data.get('department_name', instance.department_name)
        instance.department_code = validated_data.get('department_code', instance.department_code)
        instance.department_type = validated_data.get('department_type', instance.department_type)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.save()
        return instance


class SLASerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        exclude = ['id']

    def create(self, validated_data):
        # Custom create method if needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom update method if needed
        return super().update(instance, validated_data)
