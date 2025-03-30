from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsTeacher, IsStudent
from app1.models import Student, Teacher



class Register(APIView):
     def post(self, request):
          data = request.data
          serializer = RegisterSerializer(data=data)

          if not serializer.is_valid():
               return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

          user = serializer.create(serializer.validated_data)
          print(f"User Created: {user.id}, Email: {user.email}, Type: {user.utype}")

          if user.utype == 'student':
               student, created = Student.objects.get_or_create(user=user, defaults={
                    "roll_no": None,
                    "dept": None,
                    "year": None,
                    "batch": None
               })
               print(f"Student created: Student ID: {student.id}")

          elif user.utype == 'teacher':
               teacher, created = Teacher.objects.get_or_create(user=user, defaults={
                    "dept": None,
                    "year": None,
                    "salary": None
               })
               print(f"Teacher created: Teacher ID: {teacher.id}")

          return Response(data, status=status.HTTP_201_CREATED)


class Loginn(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
          email = request.data.get('email')
          password = request.data.get('password')
          user = authenticate(email=email, password=password)

          if user is not None:
               refresh = RefreshToken.for_user(user)
               return Response({
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
               },status=status.HTTP_200_OK)
          return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)





class AdminDashboardView(APIView):
     permission_classes = [IsAuthenticated, IsAdmin]

     def get(self, request):
          return Response({"message": "Welcome Admin"})


class TeacherDashboardView(APIView):
     permission_classes = [IsAuthenticated, IsTeacher]

     def get(self, request):
          return Response({"message": "Welcome Teacher"})

class StudentDashboardView(APIView):
     permission_classes = [IsAuthenticated, IsStudent]

     def get(self, request):
          return Response({"message": "Welcome Student"})







# {
# "username": "sagil",
# "password": "Sagil@123",
# "email": "sagil@gmail.com",
# "first_name": "Sagil",
# "last_name": "K",
# }
#
# {
# "username": "sarang",
# "password": "Sarang@123",
# "email": "Sarang@gmail.com",
# "utype": "teacher",
# "first_name": "Sarang",
# "last_name": "K"
# }
