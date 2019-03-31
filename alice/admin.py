from django.contrib import admin
from .models import Univercity, Group, Lesson, Dates, AliceUsers, SiteUsers, Admin
# Register your models here.




admin.site.register(Univercity)
admin.site.register(Admin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'univerсity_id')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'classroom', 'start_time', 'end_time', 'day_of_week', 'repeat', 'type', 'group_id')


class DatesAdmin(admin.ModelAdmin):
    list_display = ('date', 'lesson_id')

class AliceUsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'univerсity_id', 'group_id')

class SiteUsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'univerсity_id', 'group_id', 'admin')



admin.site.register(Group, GroupAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Dates, DatesAdmin)
admin.site.register(AliceUsers, AliceUsersAdmin)
admin.site.register(SiteUsers, SiteUsersAdmin)





