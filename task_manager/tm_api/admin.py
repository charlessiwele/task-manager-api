from django.contrib import admin
from tm_api.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        'due_date',
        'status',
        'user',
    ]
