from django.contrib import admin
from .models import Univercity, Group, Lesson, Dates
# Register your models here.


# class UnivercityAdmin(admin.ModelAdmin):
#     list_display = ('name')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'univercity_id')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'classroom', 'start_time', 'end_time', 'group_id')


class DatesAdmin(admin.ModelAdmin):
    list_display = ('date', 'lesson_id')


# admin.site.register(Univercity, UnivercityAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Dates, DatesAdmin)

#


