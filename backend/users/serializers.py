from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'user_type', 'company_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user_type = attrs.get('user_type')
        company_name = attrs.get('company_name')

        if user_type == 'seller' and not company_name:
            raise serializers.ValidationError("Sellers must provide a company name.")
        if user_type == 'buyer' and company_name:
            raise serializers.ValidationError("Buyers should not provide a company name.")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
