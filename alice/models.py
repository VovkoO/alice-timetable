from django.db import models

# Create your models here.


class Univercity(models.Model):
    name = models.CharField(max_length=50)
    readable_name = models.CharField(max_length=50, default=name)


class Group(models.Model):
    name = models.CharField(max_length=20)
    readable_name = models.CharField(max_length=20, default=name)
    univercity_id = models.ForeignKey(Univercity, on_delete=models.CASCADE, null=True, blank=True)


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=20)
    classroom = models.CharField(max_length=10)
    start_time = models.TimeField(auto_now=False, null=True)
    end_time = models.TimeField(auto_now=False, null=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)


class Dates(models.Model):
    date = models.DateField(auto_now=False)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)


class AliceUsers(models.Model):
    user_id = models.CharField(max_length=65)
    univercity_id = models.ForeignKey(Univercity, on_delete=models.CASCADE, null=True, blank=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
