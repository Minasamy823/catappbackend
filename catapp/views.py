from django.shortcuts import redirect
from rest_framework import mixins
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import *
from .permissions import *
from .serializers import *


# just for saving a user instance then redirecting the user to login page for receiving the token
class Register(APIView):

    def post(self, request):
        username = self.request.data.get('username')
        user = User.objects.filter(username=username)
        if user.exists():
            raise ValidationError('user does exist')
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
        return Response('registered')


#  list of cats that the request.user already has OR create a new instance
class CatView(APIView):
    permission_classes = [RegisteredUserPermission]

    def get(self, request):
        user = request.user
        cats = user.owner.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        age = request.data.get('age')
        owner = User.objects.get(pk=request.user.id).id
        data = [{"owner": owner, 'age': age, 'name': name}]
        serializer = CatSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response('created')
        else:
            return Response(serializer.errors)


class CatDetails(generics.RetrieveUpdateAPIView,  mixins.DestroyModelMixin):
    permission_classes = (UserIsOwnerOrReadOnly,)
    serializer_class = CatSerializer

    def get_object(self):
        id_ = self.kwargs["id"]
        obj = get_object_or_404(Cat, pk=id_)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        name = request.data.get('name')
        age = request.data.get('age')
        owner = User.objects.get(pk=request.user.id).id
        data = {"owner": owner, 'age': age, 'name': name}
        serializer = CatSerializer(data=data, instance=obj)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
