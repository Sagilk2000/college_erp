

from django.db import models
from accounts.models import User
from django.utils import timezone


class Dept(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.course_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'utype': 'student'})
    roll_no = models.IntegerField(null=True, blank=True)
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    batch = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return f"{self.user.first_name} - {self.roll_no}"

    # def update_student_data(self, roll_no=None, dept=None, year=None, batch=None):
    #     """Update missing student details"""
    #     if roll_no:
    #         self.roll_no = roll_no
    #     if dept:
    #         self.dept = dept
    #     if year:
    #         self.year = year
    #     if batch:
    #         self.batch = batch
    #     self.save()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'utype': 'teacher'})
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.user.first_name

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.email} registered for {self.course.course_name}"


class AssignCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course', 'date')


class Events(models.Model):
    event_name = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.event_name

class Exams(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()