from datetime import datetime, timedelta
from .models import Univercity, Group, Lesson, Dates, SiteUsers, Admin


def add_lesson(group, lesson_name, teacher, classroom, start_time, end_time, day_of_week, repeat, type,
               start_date, end_date):
    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()
    # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    day_of_week = int(day_of_week)
    repeat = int(repeat)

    # try:
    #     univercity = Univercity.objects.get(name=univercity_name)
    # except Univercity.DoesNotExist:
    #     readable_name = univercity_name.replace(' ', '')
    #     readable_name = readable_name.replace('-', '')
    #     readable_name = readable_name.lower()
    #     univercity = Univercity.objects.create(name=univercity_name, readable_name=readable_name)
    #
    # try:
    #     group = Group.objects.get(name=group_name, univercity_id=univercity)
    # except Group.DoesNotExist:
    #     readable_name = group_name.replace(' ', '')
    #     readable_name = readable_name.replace('-', '')
    #     readable_name = readable_name.lower()
    #     group = Group.objects.create(name=group_name, readable_name=readable_name, univercity_id=univercity)

    try:
        Lesson.objects.get(name=lesson_name, teacher=teacher, classroom=classroom, start_time=start_time,
                                    end_time=end_time, day_of_week=day_of_week, repeat=repeat, type=type, group_id=group)
        return 'Такой предмет уже существует.'
    except Lesson.DoesNotExist:
        lesson = Lesson.objects.create(name=lesson_name, teacher=teacher, classroom=classroom, start_time=start_time,
                                       end_time=end_time, day_of_week=day_of_week, repeat=repeat, type=type, group_id=group)
    return add_dates_to_db(lesson, day_of_week, repeat, start_date, end_date)


def add_dates_to_db(lesson, day_of_week, repeat, start_date, end_date):
    if repeat == 0:  # если занятие повторяется каждую неделю
        if datetime.weekday(start_date) > day_of_week:
            start_date = start_date + timedelta(7 - datetime.weekday(start_date) + day_of_week)
        elif datetime.weekday(start_date) < day_of_week:
            start_date = start_date + timedelta(day_of_week - datetime.weekday(start_date))
        while start_date < end_date:
            try:
                Dates.objects.get(date=start_date, lesson_id=lesson)
            except Dates.DoesNotExist:
                Dates.objects.create(date=start_date, lesson_id=lesson)
            start_date = start_date + timedelta(7)

    elif repeat == 1:  # если занятие проходит только по нечетным неделям
        if datetime.weekday(start_date) > day_of_week:
            start_date = start_date + timedelta(14 - datetime.weekday(start_date) + day_of_week)
        elif datetime.weekday(start_date) < day_of_week:
            start_date = start_date + timedelta(day_of_week - datetime.weekday(start_date))
        while start_date < end_date:
            try:
                Dates.objects.get(date=start_date, lesson_id=lesson)
            except Dates.DoesNotExist:
                Dates.objects.create(date=start_date, lesson_id=lesson)
            start_date = start_date + timedelta(14)

    elif repeat == 2:
        if datetime.weekday(start_date) > day_of_week:
            start_date = start_date + timedelta(7 - datetime.weekday(start_date) + day_of_week)
        elif datetime.weekday(start_date) < day_of_week:
            start_date = start_date + timedelta(day_of_week - datetime.weekday(start_date) + 7)
        while start_date < end_date:
            try:
                Dates.objects.get(date=start_date, lesson_id=lesson)
            except Dates.DoesNotExist:
                Dates.objects.create(date=start_date, lesson_id=lesson)
            start_date = start_date + timedelta(14)
    else:
        print('NO')
        return 'Не получилось добавить предмет.'
    print('YES')
    return 'Занятие успешно добавлено.'


def get_tomorrow_lessons(group):
    date = datetime.now() + timedelta(1)
    lessons = Lesson.objects.filter(group_id=group)
    dates = []
    lessons_copy = lessons
    for lesson in lessons:
        try:
            dates.append(Dates.objects.get(date=date, lesson_id=lesson))
        except Dates.DoesNotExist:
             lessons_copy = lessons_copy.exclude(pk=lesson.pk)
    lessons_copy = lessons_copy.order_by('start_time', 'end_time')
    return lessons_copy


def add_timetable(univercity_name, group_name, start_date, end_date, user):
    univercity = get_univercity(univercity_name)
    if univercity:
        group = get_group(univercity, group_name)
        if group:
            return False
        else:
            group = create_group(group_name, univercity, start_date, end_date)
            site_user = get_site_user(user)
            if site_user:
                site_user.univerсity_id = univercity
                site_user.group_id = group
                site_user.user_id = user
                site_user.admin = True
                site_user.save()
                Admin.objects.create(user_id=user, group_id=group)
            else:
                SiteUsers.objects.create(user_id=user, group_id=group, univerсity_id=univercity, admin=True)
                Admin.objects.create(user_id=user, group_id=group)
    else:
        univercity = create_univercity(univercity_name)
        group = create_group(group_name, univercity, start_date, end_date)
        site_user = get_site_user(user)
        if site_user:
            site_user.univerсity_id = univercity
            site_user.group_id = group
            site_user.user_id = user
            site_user.admin = True
            site_user.save()
            Admin.objects.create(user_id=user, group_id=group)
        else:
            SiteUsers.objects.create(user_id=user, group_id=group, univerсity_id=univercity, admin=True)
            Admin.objects.create(user_id=user, group_id=group)
    return True


def create_univercity(univercity_name):
    readable_univercity_name = univercity_name.replace(' ', '').replace('-', '').lower()
    univercity = Univercity.objects.create(name=univercity_name, readable_name=readable_univercity_name)
    return univercity


def create_group(group_name, univercity, start_date, end_date):
    readable_group_name = group_name.replace(' ', '').replace('-', '').lower()
    group = Group.objects.create(name=group_name, readable_name=readable_group_name, start_date=start_date,
                                 end_date=end_date, univerсity_id=univercity)
    return group


def get_univercity(univercity_name):
    readable_univercity_name = univercity_name.replace(' ', '').replace('-', '').lower()
    try:
        univercity = Univercity.objects.get(name=univercity_name)
    except Univercity.DoesNotExist:
        try:
            univercity = Univercity.objects.get(readable_name=readable_univercity_name)
        except Univercity.DoesNotExist:
            univercity = None
    return univercity


def get_group(univercity, group_name):
    readable_group_name = group_name.replace(' ', '').replace('-', '').lower()
    try:
        group = Group.objects.get(name=group_name, univerсity_id=univercity)
    except Group.DoesNotExist:
        try:
            group = Group.objects.get(readable_name=readable_group_name, univerсity_id=univercity)
        except Group.DoesNotExist:
            group = None
    return group


def get_site_user(user):
    try:
        site_user = SiteUsers.objects.get(user_id=user)
    except:
        site_user = None
    return site_user


def change_lesson(lesson, name, teacher, classroom, start_time, end_time, type, day_of_week, repeat, start_date, end_date):
    if lesson.name != name:
        lesson.name = name
    if lesson.teacher != teacher:
        lesson.teacher = teacher
    if lesson.classroom != classroom:
        lesson.classroom = classroom
    if lesson.start_time != start_time:
        lesson.start_time = start_time
    if lesson.end_time != end_time:
        lesson.end_time = end_time
    if lesson.type != type:
        lesson.type = type
    if lesson.day_of_week != day_of_week or lesson.repeat != repeat:
        if lesson.day_of_week != day_of_week:
            lesson.day_of_week = day_of_week
        if lesson.repeat != repeat:
            lesson.repeat = repeat
        Dates.objects.filter(lesson_id=lesson).delete()
        add_dates_to_db(lesson, day_of_week, repeat, start_date, end_date)
    lesson.save()
    return 'Предмет был изменен'



