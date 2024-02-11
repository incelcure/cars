from django.contrib.auth import authenticate
from django.forms import model_to_dict
from django.http import JsonResponse
from django_rest.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .permissions import *
from .serializers import CarSerializer


# Create your views here.
class CarApiList(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated & (IsRegularUser | IsAdminUser)]
    # permission_classes = (IsAdminOrReadOnly,)


class CarApiCreate(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    # permission_class = (IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return JsonResponse({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         else:
#             return JsonResponse({"error": "Invalid Credentials"}, status=400)

# class CarViewSet(mixins.CreateModelMixin,
#                  mixins.ListModelMixin,
#                  GenericViewSet):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#
#     @action(methods=['get'], detail=False)
#     def brands(self, request, pk=None):
#         brands = CarBrand.objects.all()
#         return Response({'brands': [b.name for b in brands]})

# class CarApiView(APIView):
#     def get(self, request):
#         c = Car.objects.all()
#         return Response({'posts': CarSerializer(c, many=True).data})
#
#     def post(self, request):
#         serializer = CarSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#         try:
#             instance = Car.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = CarSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})

# def delete(self, request, *args, **kwargs):
#     pk = kwargs.get("pk", None)
#     if not pk:
#         return Response({"error": "Method DELETE not allowed"})
#     return Response({"post": "delete post" + str(pk)})

# post_new = Car.objects.create(
#     brand_id=request.data['brand_id'],
#     model=request.data['model'],
#     description=request.data['description'],
#     #            horsepower=request.data['horsepower'],
#     mileage=request.data['mileage']
# )
# return Response({'post': CarSerializer(post_new).data})

# class CarApiView(generics.ListAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#
#     def get(self, request):
#         lst = Car.objects.all().values()
#         return Response({'posts': list(lst)})
#
#     def post(self, request):
#         post_new = Car.objects.create(
#             brand=request.data['brand'],
#             model=request.data['model'],
#             description=request.data['description'],
#             #            horsepower=request.data['horsepower'],
#             mileage=request.data['mileage']
#         )
#         return Response({'post': model_to_dict(post_new)})
