from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Student, Teacher

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):

    if created and instance.utype == 'student':
        Student.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.utype == 'teacher':
        Teacher.objects.get_or_create(user=instance, defaults={'year': 2024, 'salary': 0})