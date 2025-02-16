from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(
        max_length=50, 
        blank=False, 
        null=False,
        unique=True,
        help_text=(
            "Required. Status name, 50 characters or fewer."
        ),
        error_messages={
            "unique": ("A Status with this name already exists."),
        }
    )
    description = models.CharField(max_length=500, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=1500, blank=False, null=False)
    due_date = models.DateTimeField(default=timezone.now, blank=False, null=False)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
