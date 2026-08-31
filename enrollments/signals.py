"""
Signal handler for Enrollments App events.
"""

from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save

from .models import Enrollment


@receiver(post_save, sender=Enrollment)
def notify_student_on_enrollment_created(sender, instance, created, **kwargs):
    """Sends email notification when a student is enrolled."""

    if created:
        send_mail(
            subject=f"Enrolled in {instance.course.title}",
            message=f"Hello {instance.student.username},\n\nYou have been successfully enrolled in '{instance.course.title}'.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.student.email],
            fail_silently=False,
        )


@receiver(pre_save, sender=Enrollment)
def notify_student_on_status_change(sender, instance, **kwargs):
    """Sends email notification to student when their enrollment status changes."""

    if instance.pk:
        previous = Enrollment.objects.filter(pk=instance.pk).first()

        if previous and previous.status != instance.status:
            send_mail(
                subject=f"Status Updated for {instance.course.title}",
                message=f"Hello {instance.student.username},\n\nYour enrollment status for '{instance.course.title}' has changed to '{instance.status}'.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.student.email],
                fail_silently=False,
            )
