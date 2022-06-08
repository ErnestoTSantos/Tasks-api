from assignments.models import Assignment, Category
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestAssignmentModel(APITestCase):
    def test_name_returned(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )
        category = Category.objects.create(creator=clovis, name="Teste")

        assignment = Assignment.objects.create(
            creator=clovis,
            category=category,
            task_name="Conseguir um bom emprego",
        )

        assert str(assignment) == "Clovis -> Conseguir um bom emprego"


class TestCategoryModel(APITestCase):
    def test_category_name_returned(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        category = Category.objects.create(creator=clovis, name="Teste")

        assert str(category) == "Teste"
