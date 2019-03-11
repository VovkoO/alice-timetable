from datetime import datetime, timedelta
from .models import Univercity, Group, Lesson, Dates


def add_to_db(univercity_name, group_name, lesson_name, teacher, classroom, start_time, end_time, day_of_week,
              start_date, end_date, repeat):
    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    day_of_week = int(day_of_week)

    try:
        univercity = Univercity.objects.get(name=univercity_name)
    except Univercity.DoesNotExist:
        univercity = Univercity.objects.create(name=univercity_name)

    try:
        group = Group.objects.get(name=group_name, univercity_id=univercity)
    except Group.DoesNotExist:
        group = Group.objects.create(name=group_name, univercity_id=univercity)

    try:
        lesson = Lesson.objects.get(name=lesson_name, teacher=teacher, classroom=classroom, start_time=start_time,
                                    end_time=end_time, group_id=group)
    except Lesson.DoesNotExist:
        lesson = Lesson.objects.create(name=lesson_name, teacher=teacher, classroom=classroom, start_time=start_time,
                                       end_time=end_time, group_id=group)
    return add_dates_to_db(lesson, day_of_week, repeat, start_date, end_date)


def add_dates_to_db(lesson, day_of_week, repeat, start_date, end_date):
    if repeat == 'each_week':  # если занятие повторяется каждую неделю
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

    elif repeat == 'uneven_week':  # если занятие проходит только по четным неделям
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

    elif repeat == 'even_week':
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
        return False
    return True
