from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'owner']
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        user = self.context['request'].user
        return Company.objects.create(owner=user, **validated_data)
