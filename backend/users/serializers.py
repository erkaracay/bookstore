from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'user_type', 'company_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user_type = attrs.get("user_type")
        company_name = attrs.get("company_name")

        if user_type == "seller":
            if not company_name or company_name.strip() == "":
                raise serializers.ValidationError({"company_name": "Sellers must provide a company name."})
        elif user_type == "buyer" and company_name and company_name.strip() != "":
            raise serializers.ValidationError({"company_name": "Buyers should not provide a company name."})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
