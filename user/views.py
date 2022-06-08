from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.serializers import UserSerializer


class ListUser(generics.ListAPIView):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class DetailUser(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        username = request.user.username

        if instance.username == username:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)

        return Response(["Você não pode acessar esse usuário!"])


@api_view(http_method_names=["POST"])
def create_user(request):
    if request.method == "POST":
        data = request.data
        username = data["username"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        is_staff = data.get("is_staff", False)

        if not username:
            raise serializers.ValidationError("É necessário ter um nome de usuário!")

        if not password:
            raise serializers.ValidationError(
                "É necessário ter uma senha para o usuário!"
            )

        if not email:
            raise serializers.ValidationError(
                "É necessário ter um e-mail para o usuário!"
            )

        if not first_name:
            raise serializers.ValidationError("É necessário ter um primeiro nome!")

        if len(first_name) < 3:
            raise serializers.ValidationError(
                "O primeiro nome precisa ter mais de 3 caracteres!"
            )

        if not last_name:
            raise serializers.ValidationError("É necessário ter um sobrenome!")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("O nome de usuário enviado já existe!")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("O e-mail enviado já está em uso!")

        obj = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=is_staff,
            first_name=first_name,
            last_name=last_name,
        )

        dict_obj = {
            "id": obj.id,
            "username": obj.username,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "password": obj.password,
            "e-mail": obj.email,
            "is_staff": obj.is_staff,
        }

        return JsonResponse(dict_obj, status=201)


@api_view(http_method_names=["GET"])
def status_check(request):
    return Response({"status": "OK"}, status=200)
