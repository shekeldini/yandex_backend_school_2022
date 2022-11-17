from rest_framework import serializers

from enterprise.users.models import User, Company, Job


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            "first_name",
            "second_name",
            "last_name",
            "phone_number",
        )


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job

        fields = (
            "id",
            "title",
        )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company

        fields = (
            "id",
            "title",
            "address",
        )
