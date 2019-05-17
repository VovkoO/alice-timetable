from datetime import timedelta, datetime
from .models import Univercity, Group, Lesson, Dates, AliceUsers


def get_answer(json_request):
    user_id = json_request['session']['user_id']
    try:
        alice_user = AliceUsers.objects.get(user_id=user_id)
    #если у пользователя не указаны данные об университете и группе, то добавляем их
    except AliceUsers.DoesNotExist:
        if json_request['session']['message_id'] == 0:
            return 'Здравствуйте, для начала выберете ученое заведение. Просто скажите его название.'
        unicerciry_input = json_request['request']['command']
        try:
            univercity = Univercity.objects.get(name=unicerciry_input)
        except Univercity.DoesNotExist:
            unicerciry_input = unicerciry_input.replace(' ', '').replace('-', '')
            try:
                univercity = Univercity.objects.get(readable_name=unicerciry_input)
            except Univercity.DoesNotExist:
                return 'Не получилось найти подходящего расписания. Попробуйте произнести еще раз название заведения,' \
                       ' либо добавте свое расписание на сайте.'
        AliceUsers.objects.create(user_id=user_id, univerсity_id=univercity)
        ##Пользователь ввел университет, теперь вводит группу
        return 'Вам осталось указать группу. Произнесите ее название.'
    user_group = alice_user.group_id
    if not user_group:
        print(alice_user.group_id)
        if json_request['session']['message_id'] == 0:
            return 'Здравствуйте, для начала вам нужно выбрать группу, в которой учитесь. Просто скажите ее название.'
        group_input = json_request['request']['command']
        try:
            group = Group.objects.get(name=group_input)
        except Group.DoesNotExist:
            group_input = group_input.replace(' ', '')
            try:
                group = Group.objects.get(readable_name=group_input)
            except Group.DoesNotExist:
                return 'Не получилось найти походящего расписания. Попробуйте произнести еще раз название группы,' \
                       ' либо добавте свое расписание на сайте.'
        alice_user.group_id = group
        alice_user.save()
        return 'Вы выбрали свое расписание, теперь вы можете узнать у меня расписание на какой-либо день, ' \
               'просто скажите число, на которе вы хотите его узнать.'

    if json_request['session']['message_id'] == 0:
        return 'Здравствуйте, на какое число вы бы хотели узнать расписание?'
    if len(json_request['request']['command']) == 0:
        return 'Извините, я не поняла, на какое число вы бы хотели узнать расписание?'
    user_group = alice_user.group_id
    date = get_date(json_request)
    if date is None:
        return 'Извините, я не поняла, на какое число вы бы хотели узнать расписание?'
    print(date)
    lessons = get_lessons(date, user_group)
    if len(lessons) == 0:
        return 'У вас ' + str(date.day) + ' ' + str(date.month) + ' нет пар'
    else:
        answer = str(date.day) + ' ' + str(date.month) + ' у вас ' + str(len(lessons)) + ' пар. Сначала: '
        for lesson in lessons:
            answer = answer + ' ' + lesson.name + ' в ' + str(lesson.start_time) + ', затем: '
    return answer


def get_date(json_request):
    timezone = json_request['meta']['timezone']
    today = datetime.now()
    date_dict = None
    for token in json_request['request']['nlu']['entities']:
        if 'type' in token and token['type'] == 'YANDEX.DATETIME':
            date_dict = token['value']
            break
    if date_dict is None:   ##Обрабатываем дни недели
        words = json_request['request']['nlu']['tokens']
        day_of_week = get_day_of_week(json_request['request']['nlu']['tokens'])
        today_week_day = datetime.weekday(today)
        if day_of_week is not None:
            if 'предыдущий' in words or 'предыдущая' in words or 'предыдущую' in words or 'предыдущее' in words or \
                    'прошлый' in words or 'прошлая' in words or 'прошлую' in words or 'прошлее' in words or \
                    'была' in words or 'были' in words:
                if day_of_week == today_week_day:
                    return today - timedelta(7)
                if today_week_day > day_of_week:
                    return today - timedelta(today_week_day - day_of_week)
                if today_week_day < day_of_week:
                    return today - timedelta(7 - (day_of_week - today_week_day))
            elif 'следующий' in words or 'следующая' in words or 'следующую' in words or 'следующее' in words:
                return today + timedelta(7 - today_week_day + day_of_week)
            else:
                if day_of_week == today_week_day:
                    return today
                if today_week_day > day_of_week:
                    return today + timedelta(7 - today_week_day + day_of_week)
                if today_week_day < day_of_week:
                    return today + timedelta(day_of_week - today_week_day)


    else:   ##Если в запросе уже есть данные о дате
        if 'day_is_relative' in date_dict:
            if date_dict['day_is_relative']:
                return today + timedelta(date_dict['day'])
            else:
                day = date_dict['day']
        else:
            day = today.day

        if 'year_is_relative' in date_dict and not date_dict['year_is_relative']:
            year = int(date_dict['year'])
        else:
            year = today.year

        if 'month_is_relative' in date_dict and not date_dict['month_is_relative']:
            month = int(date_dict['month'])
        else:
            month = today.month
        return datetime(year, month, day)

    if 'расписание' in json_request['request']['nlu']['tokens'] or 'пары' in json_request['request']['nlu']['tokens']:
        return datetime.now()

    return None


def get_day_of_week(words):
    if 'понедельник' in words:
        return 0
    if 'вторник' in words:
        return 1
    if 'среда' in words or 'среду' in words:
        return 2
    if 'четверг' in words:
        return 3
    if 'пятница' in words or 'пятницу' in words:
        return 4
    if 'суббота' in words or 'субботу' in words:
        return 5
    if 'воскресенье' in words:
        return 6
    return None


def get_lessons(date, group):
    lessons = Lesson.objects.filter(group_id=group)
    print(lessons)
    dates = []
    lessons_copy = lessons
    for lesson in lessons:
        try:
            dates.append(Dates.objects.get(date=date, lesson_id=lesson))
        except Dates.DoesNotExist:
             lessons_copy = lessons_copy.exclude(pk=lesson.pk)
    lessons_copy = lessons_copy.order_by('start_time', 'end_time')
    print(lessons_copy)
    return lessons_copy
