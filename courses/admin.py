from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "duration_value", "duration_unit", "schedule", "created_at")
    list_filter = ("teacher",)
    search_fields = ("title", "description")
