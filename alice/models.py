from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Univercity(models.Model):
    name = models.CharField(max_length=50)
    readable_name = models.CharField(max_length=50, default=name)


class Group(models.Model):
    name = models.CharField(max_length=20)
    readable_name = models.CharField(max_length=20, default=name)
    start_date = models.DateField(auto_now=False, null=True)
    end_date = models.DateField(auto_now=False, null=True)
    univerсity_id = models.ForeignKey(Univercity, on_delete=models.CASCADE, null=True, blank=True)


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=20, blank=True)
    classroom = models.CharField(max_length=10, blank=True)
    start_time = models.TimeField(auto_now=False, null=True)
    end_time = models.TimeField(auto_now=False, null=True)
    day_of_week = models.IntegerField(default=0)
    repeat = models.IntegerField(default=0)
    type = models.CharField(max_length=10, blank=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)


class Dates(models.Model):
    date = models.DateField(auto_now=False)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)


class AliceUsers(models.Model):
    user_id = models.CharField(max_length=65)
    univerсity_id = models.ForeignKey(Univercity, on_delete=models.CASCADE, null=True, blank=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)


class SiteUsers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    univerсity_id = models.ForeignKey(Univercity, on_delete=models.CASCADE, null=True, blank=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.BooleanField(default=False)


class Admin(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)