import json

from assignments.models import Assignment, Category
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestingAssignmentView(APITestCase):
    def test_get_empty_assignment_list(self):
        user = User.objects.create(username="Ernesto", password="12345")
        self.client.force_authenticate(user)
        request = self.client.get("/api/assignment/list_assignments/")
        data = json.loads(request.content)

        assert data == []

    def test_get_assignment_list(self):
        user = User.objects.create(username="Ernesto", password="12345")
        self.client.force_authenticate(user)

        category = Category.objects.create(creator=user, name="Teste")
        Assignment.objects.create(
            creator=user, category=category, task_name="Criar projeto to-do"
        )

        request = self.client.get("/api/assignment/list_assignments/?username=Ernesto")
        data = json.loads(request.content)

        assignment_return = {
            "active": True,
            "category": 1,
            "category_link": "http://testserver/api/assignment/category/1/",
            "create_day": "2022-06-07",
            "creator": "Ernesto",
            "description": "",
            "id": 1,
            "task_name": "Criar projeto to-do",
            "final_day": None,
        }

        assert data[0] == assignment_return

    def test_post_assignment(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        Category.objects.create(creator=clovis, name="Teste")

        assignment = {
            "creator": "Clovis",
            "category": 1,
            "task_name": "Fazer prova de cálculo 1",
        }

        self.client.force_authenticate(clovis)
        request_post = self.client.post("/api/assignment/list_assignments/", assignment)

        assert request_post.status_code == 201

    def test_retrive_assignment(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        category = Category.objects.create(creator=clovis, name="Teste")
        Assignment.objects.create(
            creator=clovis, category=category, task_name="Criar projeto to-do"
        )

        self.client.force_authenticate(clovis)
        request = self.client.get("/api/assignment/assignment_details/1/")

        assert request.status_code == 200

    def test_retrive_not_allowed_assignment(self):
        user = User.objects.create(username="Ernesto", password="12345")
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        category = Category.objects.create(creator=clovis, name="Teste")
        Assignment.objects.create(
            creator=clovis, category=category, task_name="Criar projeto to-do"
        )

        self.client.force_authenticate(user)
        request = self.client.get("/api/assignment/assignment_details/1/")

        assert request.data == ["Você não tem permissão para acessar essa tarefa!"]

    def test_destroy_assignment(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        category = Category.objects.create(creator=clovis, name="Teste")
        Assignment.objects.create(
            creator=clovis, category=category, task_name="Criar projeto to-do"
        )

        self.client.force_authenticate(clovis)
        request = self.client.delete("/api/assignment/assignment_details/1/")

        assert request.status_code == 204

    def test_destroy_not_allowed_assignment(self):
        user = User.objects.create(username="Ernesto", password="12345")
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        category = Category.objects.create(creator=clovis, name="Teste")
        Assignment.objects.create(
            creator=clovis, category=category, task_name="Criar projeto to-do"
        )

        self.client.force_authenticate(user)
        request = self.client.delete("/api/assignment/assignment_details/1/")

        assert request.data == ["Você não tem permissão para deletar essa tarefa!"]


class TestCategoryView(APITestCase):
    def test_list_category(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        Category.objects.create(creator=clovis, name="Teste")

        self.client.force_authenticate(clovis)
        request = self.client.get("/api/assignment/category/")

        assert request.status_code == 200

    def test_create_category(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        category = {"creator": "Clovis", "name": "Teste"}

        self.client.force_authenticate(clovis)
        request = self.client.post("/api/assignment/category/", category)

        assert request.status_code == 201

    def test_retrive_category(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        Category.objects.create(creator=clovis, name="Teste")

        self.client.force_authenticate(clovis)
        request = self.client.get("/api/assignment/category/1/")

        assert request.status_code == 200

    def test_destroy_category(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )

        Category.objects.create(creator=clovis, name="Teste")

        self.client.force_authenticate(clovis)
        request = self.client.delete("/api/assignment/category/1/")

        assert request.status_code == 204

    def test_destroy_not_allowed(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )
        user = User.objects.create(
            username="Ernesto", password="12345", email="ernesto@gmail.com"
        )

        Category.objects.create(creator=clovis, name="Teste")

        self.client.force_authenticate(user)
        request = self.client.delete("/api/assignment/category/1/")

        assert request.data == ["Você não tem permissão para deletar essa categoria!"]

    def test_retrieve_not_allowed(self):
        clovis = User.objects.create(
            username="Clovis", password="12345", email="Clovis@gmail.com"
        )
        user = User.objects.create(
            username="Ernesto", password="12345", email="ernesto@gmail.com"
        )

        Category.objects.create(creator=clovis, name="Teste")

        self.client.force_authenticate(user)
        request = self.client.get("/api/assignment/category/1/")

        assert request.data == ["Você não tem permissão para acessar essa categoria!"]


class TestStatusCheck(APITestCase):
    def test_assignment_status_check(self):
        request = self.client.get("/api/assignment/")

        assert request.status_code == 200
