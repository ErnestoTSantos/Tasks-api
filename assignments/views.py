from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from assignments.models import Assignment, Category
from assignments.serializers import AssignmentSerializer, CategorySerializer


class ListAssignments(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if settings.TESTING is not True:
            data["creator"] = str(request.user)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        category = Category.objects.filter(id=data["category"]).first()
        category.used += 1
        category.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_queryset(self):
        username = self.request.user.username

        qs = Assignment.objects.filter(creator__username=username)
        return qs


class AssignmentDetails(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer
    lookup_field = "id"
    queryset = Assignment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        username = self.request.user.username

        if instance.creator.username == username:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(["Você não tem permissão para acessar essa tarefa!"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = self.request.user.username

        if instance.creator.username == username:
            self.perform_destroy(instance)
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(["Você não tem permissão para deletar essa tarefa!"])


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.request.user.username
        qs = Category.objects.filter(creator__username=username)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        username = self.request.user.username

        if instance.creator.username == username:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(["Você não tem permissão para acessar essa categoria!"])

    def create(self, request, *args, **kwargs):
        data = request.data
        if settings.TESTING is not True:
            data["creator"] = str(request.user)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = self.request.user.username

        if instance.creator.username == username:
            self.perform_destroy(instance)
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(["Você não tem permissão para deletar essa categoria!"])


@api_view(http_method_names=["GET"])
def status_check(request):
    return Response({"status": "OK"}, status=200)
