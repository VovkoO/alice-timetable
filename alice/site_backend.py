from datetime import datetime, timedelta
from .models import Univercity, Group, Lesson, Dates


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
        return 'Не получилось добавить предмет.'
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