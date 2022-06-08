from django.contrib import admin

from assignments.models import Assignment, Category


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "task_name",
        "category",
        "create_day",
        "final_day",
        "active",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "used")
