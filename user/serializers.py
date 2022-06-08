from assignments.serializers import AssignmentSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
        ]


class AssignmentsUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "assignment"]

    assignment = AssignmentSerializer(many=True, read_only=True)
