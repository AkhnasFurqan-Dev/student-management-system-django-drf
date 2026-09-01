"""
Signal handler for Courses App events.
"""

from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import pre_save

from .models import Course


@receiver(pre_save, sender=Course)
def notify_teacher_on_assignment(sender, instance, **kwargs):
    """Sends email to the teacher when they are assigned to the course."""

    if not instance.teacher:
        return

    if instance.pk:
        previous = Course.objects.filter(pk=instance.pk).first()

        if previous and previous.teacher == instance.teacher:
            return

    send_mail(
        subject=f"Assigned to Course: {instance.title}",
        message=f"Hello {instance.teacher.username},\n\nYou have been assigned as the instructor for the course '{instance.title}'.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.teacher.email],
        fail_silently=False,
    )
