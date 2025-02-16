from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from tm_api.models import Task, Status


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ["id", "name", "description"]


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def save(self):
        try:
            user = User.objects.filter(
                username=self.data['username'],
            ).first()
            if user:
                raise LookupError("Username already exists")

            user = User.objects.filter(
                email=self.data['email']
            ).first()

            if user:
                raise LookupError("Email already exists")

            user = User.objects.create(
                email=self.data['email'],
                username=self.data['username']
            )
            user.set_password(self.data['password'])
            user.save()
            return user
    
        except Exception as exception:
            return str(exception)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status']

    def save(self, request):
        title=self.data.get('title')
        description=self.data.get('description')
        due_date=self.data.get('due_date')
        status=Status.objects.get(pk=self.data.get('status')) if self.data.get('status') else None
        user=User.objects.get(pk=request.user.pk)
        try:
            with transaction.atomic():
                task = Task.objects.create(
                    title=title,
                    description=description,
                    due_date=due_date,
                    status=status,
                    user=user
                )
                return task
        except Exception as exception:
            return str(exception)

