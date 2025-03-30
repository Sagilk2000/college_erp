from rest_framework import serializers
from .models import Course, CourseRegistration, AssignCourse, Dept, Student, Teacher, Marks, Attendance, Events, Exams


class StudentSerializer(serializers.ModelSerializer):
    dept_id = serializers.IntegerField(write_only=True, required=False)  # Accept dept_id in request

    class Meta:
        model = Student
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     # Extract dept_id from request data
    #     dept_id = validated_data.pop('dept_id', None)
    #
    #     if dept_id:
    #         try:
    #             dept = Dept.objects.get(id=dept_id)  # Fetch Dept instance
    #             instance.dept = dept  # Assign to Student model
    #         except Dept.DoesNotExist:
    #             raise serializers.ValidationError({"dept_id": "Invalid department ID."})
    #
    #     # Update other fields
    #     return super().update(instance, validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = '__all__'

class AssignCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignCourse
        fields = '__all__'

class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dept
        fields = '__all__'

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['status']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class CourseAttendanceSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_name = serializers.CharField()
    total_classes = serializers.IntegerField()
    attended_classes = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()

class ExamSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = '__all__'