from datetime import date

from django.contrib.auth.models import User
from rest_framework import serializers

from assignments.models import Assignment, Category


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "id",
            "creator",
            "task_name",
            "category",
            "category_link",
            "description",
            "create_day",
            "final_day",
            "active",
        ]

    creator = serializers.CharField(max_length=50)
    category_link = serializers.HyperlinkedRelatedField(
        many=False,
        source="category",
        view_name="assignments:category-detail",
        read_only=True,
    )

    def validate_creator(self, value):
        obj = User.objects.filter(username=value)

        return obj.first()

    def validate_task_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "O nome da tarefa precisa ter 5 ou mais caracteres!"
            )

        return value

    def validate_final_day(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "A finalização não pode ser realizada no passado!"
            )

        return value

    def validate(self, attrs):
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "creator", "name", "used"]

    creator = serializers.CharField(max_length=50)

    def validate_creator(self, value):
        obj = User.objects.filter(username=value)

        return obj.first()

    def validate(self, attrs):
        creator = attrs["creator"]
        name = attrs["name"]

        if Category.objects.filter(creator=creator, name=name):
            raise serializers.ValidationError(f'A categoria "{name}" já existe!')

        return attrs
