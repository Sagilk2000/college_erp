# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Count, Q
#
# class StudentAttendanceView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         try:
#             student = Student.objects.get(user=user)
#         except Student.DoesNotExist:
#             return Response({"error": "Student profile not found."}, status=404)
#
#         # Retrieve courses the student is registered in
#         registered_courses = CourseRegistration.objects.filter(student=student).select_related('course')
#
#         attendance_data = []
#
#         for registration in registered_courses:
#             course = registration.course
#             total_classes = Attendance.objects.filter(course=course).count()
#             attended_classes = Attendance.objects.filter(course=course, student=student, status=True).count()
#             attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
#
#             attendance_data.append({
#                 'course_id': course.id,
#                 'course_name': course.name,
#                 'total_classes': total_classes,
#                 'attended_classes': attended_classes,
#                 'attendance_percentage': attendance_percentage,
#             })
#
#         serializer = CourseAttendanceSerializer(attendance_data, many=True)
#         return Response(serializer.data)
