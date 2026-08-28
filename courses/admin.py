from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "duration", "schedule", "created_at")
    list_filter = ("teacher",)
    search_fields = ("title", "description")
