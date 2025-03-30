from django.urls import path
from .views import AddCourse, CourseRegistrationView, CourseView, UpdateStudentData, AssignCourseToTeacher, AddDepartment, UpdateTeacher, RegisteredCoursesView, TeacherCourses, AssignMark, StudentMarksView, UpdateDepartmentView, MarkAttendance, UpdateAttendance, AddEventsView, EventView, StudentAttendanceView, AddExams, UpdateExam, StudentExamView
urlpatterns = [
    path('add_course', AddCourse.as_view(), name='add_course'),
    path('course_reg', CourseRegistrationView.as_view(), name='course_reg'),
    path('course_view', CourseView.as_view(), name='course_view'),
    path('update_student', UpdateStudentData.as_view(), name='update_student'),
    path('assign_courses', AssignCourseToTeacher.as_view(), name='assign_courses'),
    path('add_dept', AddDepartment.as_view(), name='add_dept'),
    path('update_dept/<int:dept_id>/', UpdateDepartmentView.as_view(), name='update_dept'),
    path('update_teacher', UpdateTeacher.as_view(), name='update_teacher'),
    path('registered_course', RegisteredCoursesView.as_view(), name='registered_course'),
    path('teacher_courses', TeacherCourses.as_view(), name='teacher_courses'),
    path('assign_marks', AssignMark.as_view(), name='assign_marks'),
    path('mark_view', StudentMarksView.as_view(), name='mark_view'),
    path('mark_attendance', MarkAttendance.as_view(), name='mark_attendance'),
    path('update_attendance/<int:attendance_id>/', UpdateAttendance.as_view(), name='update_attendance'),
    path('add_events', AddEventsView.as_view(), name='add_events'),
    path('view_events', EventView.as_view(), name='view_events'),
    path('student_attendance', StudentAttendanceView.as_view(), name='student_attendance'),
    path('add_exams', AddExams.as_view(), name='add_exams'),
    path('update_exams/<int:exams_id>/', UpdateExam.as_view(), name='update_exams'),
    path('student_exam_view', StudentExamView.as_view(), name='student_exam_view'),

]