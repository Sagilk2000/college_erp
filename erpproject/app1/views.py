import generics as generics
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsStudent, IsTeacher
from .serializer import CourseSerializer, CourseRegistrationSerializer, DeptSerializer, TeacherSerializer, StudentSerializer, AssignCourseSerializer, MarkSerializer, AttendanceSerializer, AttendanceUpdateSerializer, EventSerializer, CourseAttendanceSerializer, ExamSerilizer
from rest_framework.response import Response
from .models import Course, Student, CourseRegistration, Teacher, Dept, AssignCourse, Marks, Attendance, Events, Exams
import os

class AddCourse(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Course added successfully", "course": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddDepartment(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = DeptSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Deparment Added Successfully", "department name": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateDepartmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, dept_id):
        try:
            department = Dept.objects.get(id=dept_id)
        except Dept.DoesNotExist:
            return Response({"error":"Department not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeptSerializer(department, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Department update successfully", "updated_data":serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Check if the user is a student
        if hasattr(user, 'student'):
            student = user.student
            courses = Course.objects.filter(dept=student.dept)  # Show only courses in the student's department
        else:
            courses = Course.objects.all()  # Admins, teachers, etc. see all courses

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseRegistrationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CourseRegistrationSerializer

    def post(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'only student can register the course'}, status=status.HTTP_403_FORBIDDEN)

        if not student.roll_no or not student.year or not student.batch:
            return Response(
                {'error': 'Please complete your student profile before registering for a course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        course_id = request.data.get('course')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error':'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        if CourseRegistration.objects.filter(student=student, course=course).exists():
            return Response({'error':'You are already registered this course'}, status=status.HTTP_400_BAD_REQUEST)

        registration = CourseRegistration.objects.create(student=student, course=course)
        return Response(CourseRegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)



class RegisteredCoursesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"error":"Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

        registrations = CourseRegistration.objects.filter(student=student)
        serializer = CourseRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UpdateStudentData(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student data updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UpdateStudentData(APIView):
#     permission_classes = [IsAuthenticated, IsStudent]
#
#     def post(self, request):
#         try:
#             student = Student.objects.get(user=request.user)
#         except Student.DoesNotExist:
#             return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         roll_no = request.data.get("roll_no")
#         dept_id = request.data.get("dept_id")
#         year = request.data.get("year")
#         batch = request.data.get("batch")
#
#         if dept_id:
#             try:
#                 dept = Dept.objects.get(id=dept_id)
#                 student.dept = dept
#             except Dept.DoesNotExist:
#                 return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         if roll_no is not None:
#             student.roll_no = roll_no
#         if year is not None:
#             student.year = year
#         if batch is not None:
#             student.batch = batch
#
#         student.save()
#         return Response({"message": "Student data updated successfully"}, status=status.HTTP_200_OK)

# class UpdateStudentData(APIView):
#     permission_classes = [IsAuthenticated, IsStudent]
#
#     def post(self, request):
#         try:
#             student = Student.objects.get(user=request.user)
#         except Student.DoesNotExist:
#             return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         roll_no = request.data.get("roll_no")
#         dept_id = request.data.get("dept_id")
#         year = request.data.get("year")
#         batch = request.data.get("batch")
#
#         if dept_id:
#             try:
#                 dept = Dept.objects.get(id=dept_id)
#                 student.dept = dept
#             except Dept.DoesNotExist:
#                 return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         if roll_no is not None:
#             student.roll_no = roll_no
#         if year is not None:
#             student.year = year
#         if batch is not None:
#             student.batch = batch
#
#         student.save()
#         return Response({"message": "Student data updated successfully"})
#
# class UpdateTeacher(APIView):
#     permission_classes = [IsAuthenticated, IsTeacher]
#     def post(self, request):
#         try:
#             teacher = Teacher.objects.get(user=request.user)
#         except Teacher.DoesNotExist:
#             return Response({"error": "Teacher profile not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         dept_id = request.data.get("dept_id")
#         year = request.data.get("year")
#         salary = request.data.get("salary")
#         dept_id
#         if dept_id:
#             try:
#                 dept = Dept.objects.get(id=dept_id)
#                 teacher.dept = dept
#             except Dept.DoesNotExist:
#                 return Response({"error": "Invalid DepartmentID"}, status=status.HTTP_404_NOT_FOUND)
#
#             if year is not None:
#                 teacher.year = year
#
#             if salary is not None:
#                 teacher.salary =salary
#
#             teacher.save()
#             return Response({"message":"Teacher data updated successfully"}, status=status.HTTP_200_OK)

class UpdateTeacher(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Teacher data updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AssignCourse(APIView):
#     permission_classes = [IsAdmin]
#
#     def post(self, request):
#         teacher_id = request.data.get('teacher_id')
#         course_ids = request.data.get('course_ids', [])
#         if not isinstance(course_ids, list):
#             return Response({"error": "Invalid course IDs format"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             teacher = Teacher.objects.get(id=teacher_id)
#         except Teacher.DoesNotExist:
#             return Response({"error" :"Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         courses = Course.objects.filter(id__in=course_ids)
#         if not courses.exists():
#             return Response({"error":"No valid course found"}, status=status.HTTP_400_BAD_REQUEST)
#
#         teacher.course.set(courses)
#         return Response({"message":"Course assigned successfully"}, status=status.HTTP_200_OK)


class AssignCourseToTeacher(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        teacher_id = request.data.get('teacher_id')
        course_ids = request.data.get('course_ids', [])

        if not isinstance(course_ids, list):
            return Response({"error": "Invalid course IDs format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.filter(id__in=course_ids)
        if not courses.exists():
            return Response({"error": "No valid course found"}, status=status.HTTP_400_BAD_REQUEST)

        assigned_courses = []
        for course in courses:
            assign_course, created = AssignCourse.objects.get_or_create(teacher=teacher, course=course)
            assigned_courses.append(assign_course)

        serializer = AssignCourseSerializer(assigned_courses, many=True)
        return Response({"message": "Courses assigned successfully", "data": serializer.data}, status=status.HTTP_200_OK)


class TeacherCourses(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({"error":" Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        assigned_course = AssignCourse.objects.filter(teacher=teacher)
        serializer = AssignCourseSerializer(assigned_course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignMark(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher = Teacher.objects.get(user=request.user)
        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")
        marks_obtained = request.data.get("marks_obtained")

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error":"Student Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error":"Course Not Found"}, status=status.HTTP_404_NOT_FOUND)


        if not AssignCourse.objects.filter(teacher=teacher, course=course).exists():
            return Response({"error":"you are not assign to this course"}, status=status.HTTP_403_FORBIDDEN)

        if not CourseRegistration.objects.filter(student=student, course=course).exists():
            return Response({"error":"Student not registerd for this course"}, status=status.HTTP_400_BAD_REQUEST)


        marks, created = Marks.objects.update_or_create(
            student=student, course=course, defaults={"teacher":teacher, "marks_obtained": marks_obtained}
        )

        return Response(MarkSerializer(marks).data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

class StudentMarksView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"error":"Student profile not found"}, status=status.HTTP_404_NOT_FOUND)

        marks = Marks.objects.filter(student=student)
        serializer = MarkSerializer(marks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkAttendance(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher = Teacher.objects.get(user = request.user)
        course_id = request.data.get("course_id")
        student_id = request.data.get("student_id")
        attendance_status = int(request.data.get("status", 0))
        date = request.data.get("date")

        if not date:
            return Response({"error":"date is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not AssignCourse.objects.filter(teacher=teacher, course_id=course_id).exists():
            return Response({"error": "You are not assigned to this course"}, status=status.HTTP_403_FORBIDDEN)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error":"Course not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return  Response({"error": "student not found"}, status=status.HTTP_404_NOT_FOUND)

        if not CourseRegistration.objects.filter(student=student, course=course).exists():
            return Response({"error": "Student is not registered this course"}, status=status.HTTP_400_BAD_REQUEST)

        attendance, created = Attendance.objects.get_or_create(student=student, course=course, teacher=teacher, date=date, defaults={"status": attendance_status})

        if not created:
            attendance.status = status
            attendance.save()

        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)


class UpdateAttendance(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def put(self, request, attendance_id):
        teacher = get_object_or_404(Teacher, user=request.user)
        attendance = get_object_or_404(Attendance, id=attendance_id, teacher=teacher)

        stats = request.data.get("status")
        if stats is None:
            return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendance.status = int(stats)
        except ValueError:
            return Response({"error": "Invalid status value; must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        attendance.save()
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_200_OK)



class AddEventsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event added successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        registered_courses = CourseRegistration.objects.filter(student=student).select_related('course')

        attendance_data = []

        for registration in registered_courses:
            course = registration.course
            total_classes = Attendance.objects.filter(course=course).count()
            attended_classes = Attendance.objects.filter(course=course, student=student, status=True).count()
            attendance_percentage = (attended_classes/total_classes * 100)if total_classes > 0 else 0

            attendance_data.append({
                'course_id': course.id,
                'course_name': course.course_name,
                'total_classes': total_classes,
                'attended_classes': attended_classes,
                'attendance_percentage': attendance_percentage
            })

        serializer = CourseAttendanceSerializer(attendance_data, many=True)
        return Response(serializer.data)

class AddExams(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = ExamSerilizer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateExam(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, exams_id):
        try:
            exams = Exams.objects.get(id=exams_id)
        except Exams.DoesNotFound:
            return Response({"error": "No such Exam "}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExamSerilizer(exams, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Exam details update successfully", "Updated data":serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentExamView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        registered_course = CourseRegistration.objects.filter(student=student).values_list('course_id', flat=True)

        exams = Exams.objects.filter(course_id__in=registered_course)
        serializer = ExamSerilizer(exams, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

