from datetime import timedelta, datetime
from .models import Univercity, Group, Lesson, Dates, AliceUsers
import random


def get_answer(json_request):
    user_id = json_request['session']['user_id']
    try:
        alice_user = AliceUsers.objects.get(user_id=user_id)
    #если у пользователя не указаны данные об университете и группе, то добавляем их
    except AliceUsers.DoesNotExist:
        if json_request['session']['message_id'] == 0:
            text = 'Здравствуйте, для начала выберете учебное заведение. Просто скажите его название.'
            return text, text

        ##ВВод университета
        unicerciry_input = json_request['request']['command']
        try:
            univercity = Univercity.objects.get(name=unicerciry_input)
        except Univercity.DoesNotExist:
            unicerciry_input = unicerciry_input.replace(' ', '').replace('-', '').lower()
            try:
                univercity = Univercity.objects.get(readable_name=unicerciry_input)
            except Univercity.DoesNotExist:
                univer_number = 0
                for token in json_request['request']['nlu']['entities']:
                    if 'type' in token and token['type'] == 'YANDEX.NUMBER':
                        univer_number = token['value']
                        break
                if univer_number:
                    try:
                        univercity = Univercity.objects.get(pk=univer_number)
                    except Univercity.DoesNotExist:
                        text = 'Не получилось найти подходящего расписания. Попробуйте произнести еще раз название заведения,' \
                               ' либо добавьте своё расписание на сайте alicetime.ru.'
                        return text, text
                else:
                    text = 'Не получилось найти подходящего расписания. Попробуйте произнести еще раз название заведения,' \
                           ' либо добавьте своё расписание на сайте alicetime.ru.'
                    return text, text
        AliceUsers.objects.create(user_id=user_id, univerсity_id=univercity)
        ##Пользователь ввел университет, теперь вводит группу
        text = 'Вам осталось указать группу. Произнесите её название.'
        return text, text

    ##Ввод группы
    user_group = alice_user.group_id
    if not user_group:
        if json_request['session']['message_id'] == 0:
            text = 'Здравствуйте, для начала вам нужно выбрать группу, в которой учитесь. Просто скажите её название.'
            return text, text
        group_input = json_request['request']['command']
        groups = Group.objects.filter(univerсity_id=alice_user.univerсity_id)
        try:
            group = groups.get(name=group_input)
        except Group.DoesNotExist:
            group_input = group_input.replace(' ', '').replace('-', '').lower()
            try:
                group = groups.get(readable_name=group_input)
            except Group.DoesNotExist:
                group_number = 0
                for token in json_request['request']['nlu']['entities']:
                    if 'type' in token and token['type'] == 'YANDEX.NUMBER':
                        group_number = token['value']
                        break
                if group_number:
                    try:
                        group = groups.get(pk=group_number)
                    except Group.DoesNotExist:
                        text = 'Не получилось найти подходящего расписания. Попробуйте произнести еще раз название группы,' \
                               ' либо добавьте своё расписание на сайте alicetime.ru.'
                        return text, text
                else:
                    text = 'Не получилось найти подходящего расписания. Попробуйте произнести еще раз название группы,' \
                           ' либо добавьте своё расписание на сайте alicetime.ru.'
                    return text, text
        alice_user.group_id = group
        alice_user.save()
        text = 'Вы выбрали свое расписание, теперь вы можете узнать у меня расписание на какой-либо день, ' \
               'просто скажите число, на которе вы хотите его узнать.'
        return text, text


    ##Помощь
    if 'помощь' in json_request['request']['command'] or 'Помощь' in json_request['request']['command']:
        text = 'Вы можете спросить у меня расписание на какой-нибудь день, например, сказать: "расписание на завтра", ' \
               'или выбрать другое расписание, сказав: "выбрать другое расписание".'
        return text, text

    ##Смена расписания
    words = ['сменить', 'смени', 'заменить', 'замени', 'выбрать другое', 'выбери другое']
    if any([key in json_request['request']['command'] for key in words]):
        alice_user.delete()
        text = 'Теперь выберете учебное заведение. Просто произнесите его название.'
        return text, text

    ##Получение расписания
    if json_request['session']['message_id'] == 0:
        text = 'Здравствуйте, на какое число вы бы хотели узнать расписание?'
        return text, text
    if len(json_request['request']['command']) == 0:
        text = 'Извините, я не поняла, на какое число вы бы хотели узнать расписание?'
        return text, text
    user_group = alice_user.group_id
    date = get_date(json_request)
    if date is None:
        text = 'Извините, я не поняла, на какое число вы бы хотели узнать расписание?'
        return text, text
    lessons = get_lessons(date, user_group)
    text, text_to_speech = get_nice_answer(date, lessons)
    return text, text_to_speech


def get_date(json_request):
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
    dates = []
    lessons_copy = lessons
    for lesson in lessons:
        try:
            dates.append(Dates.objects.get(date=date, lesson_id=lesson))
        except Dates.DoesNotExist:
             lessons_copy = lessons_copy.exclude(pk=lesson.pk)
    lessons_copy = lessons_copy.order_by('start_time', 'end_time')
    return lessons_copy


def get_nice_answer(date, lessons):
    text = ''
    text_to_speech = ''

    ##Обработка дня недели
    weekday = date.weekday()
    if weekday == 0:
        day_of_week = 'В понедельник '
    elif weekday == 1:
        day_of_week = 'Во вторник '
    elif weekday == 2:
        day_of_week = 'В среду '
    elif weekday == 3:
        day_of_week = 'В четверг '
    elif weekday == 4:
        day_of_week = 'В пятницу '
    elif weekday == 5:
        day_of_week = 'В субботу '
    elif weekday == 6:
        day_of_week = 'В воскресенье '
    else:
        day_of_week = ''


    ##Обработка месяца
    month_number = date.month
    if month_number == 1:
        month = 'января '
    elif month_number == 2:
        month = 'февраля '
    elif month_number == 3:
        month = 'марта '
    elif month_number == 4:
        month = 'апреля '
    elif month_number == 5:
        month = 'мая '
    elif month_number == 6:
        month = 'июня '
    elif month_number == 7:
        month = 'июля '
    elif month_number == 8:
        month = 'августа '
    elif month_number == 9:
        month = 'сентября '
    elif month_number == 10:
        month = 'октября '
    elif month_number == 11:
        month = 'ноября '
    elif month_number == 12:
        month = 'декабря '
    else:
        month = ''


    ##Обработка числа
    day_number = date.day
    if day_number == 1:
        day = 'первого '
    elif day_number == 2:
        day = 'второго '
    elif day_number == 3:
        day = 'третьего '
    elif day_number == 4:
        day = 'четвёртого '
    elif day_number == 5:
        day = 'пятого '
    elif day_number == 6:
        day = 'шестого '
    elif day_number == 7:
        day = 'седьмого '
    elif day_number == 8:
        day = 'восьмого '
    elif day_number == 9:
        day = 'девятого '
    elif day_number == 10:
        day = 'десятого '
    elif day_number == 11:
        day = 'одиннадцатого '
    elif day_number == 12:
        day = 'двенадцатого '
    elif day_number == 13:
        day = 'тринадцатого '
    elif day_number == 14:
        day = 'четырнадцатого '
    elif day_number == 15:
        day = 'пятнадцатого '
    elif day_number == 16:
        day = 'шестнадцатого '
    elif day_number == 17:
        day = 'семнадцатого '
    elif day_number == 18:
        day = 'восемнадцатого '
    elif day_number == 19:
        day = 'девятнадцатого '
    elif day_number == 20:
        day = 'двадцатого '
    elif day_number == 21:
        day = 'двадцать первого '
    elif day_number == 22:
        day = 'двадцать второго '
    elif day_number == 23:
        day = 'двадцать третьего '
    elif day_number == 24:
        day = 'двадцать четвёртого '
    elif day_number == 25:
        day = 'двадцать пятого '
    elif day_number == 26:
        day = 'двадцать шестого '
    elif day_number == 27:
        day = 'двадцать седьмого '
    elif day_number == 28:
        day = 'двадцать восьмого '
    elif day_number == 29:
        day = 'двадцать девятого '
    elif day_number == 30:
        day = 'тридцатого '
    elif day_number == 31:
        day = 'тридцать первого '
    else:
        day = ''


    ## Обработка количества занятий
    number_of_lessons = len(lessons)
    if number_of_lessons == 1:
        lessons_number = 'одно занятие: '
    elif number_of_lessons == 2:
        lessons_number = 'два занятия. '
    elif number_of_lessons == 3:
        lessons_number = 'три занятия. '
    elif number_of_lessons == 4:
        lessons_number = 'четыре занятия. '
    elif number_of_lessons == 5:
        lessons_number = 'пять занятий. '
    elif number_of_lessons == 6:
        lessons_number = 'шесть занятий. '
    elif number_of_lessons == 7:
        lessons_number = 'семь занятиий. '
    elif number_of_lessons == 8:
        lessons_number = 'восемь занятий. '
    elif number_of_lessons == 9:
        lessons_number = 'девять занятий. '
    elif number_of_lessons == 10:
        lessons_number = 'десять занятий. '


    ##обработка text_to_speech
    if number_of_lessons == 0:
        text_to_speech = day_of_week + day + month + 'у вас нет занятий. Можете отдохнуть.'
    else:
        text_to_speech = day_of_week + day + month + 'у вас ' + lessons_number
        if number_of_lessons == 1:
            text_to_speech += lessons[0].name + ' в ' + str(lessons[0].start_time)
        else:
            variants = ['потом ', 'затем ', 'после ', 'далее ']
            text_to_speech += 'Сначала ' + lessons[0].name + ' в ' + get_time(lessons[0].start_time) + ', '
            for i in range(1, number_of_lessons):
                text_to_speech += random.choice(variants)
                if i == number_of_lessons - 1:
                    text_to_speech += lessons[i].name + ' в ' + get_time(lessons[i].start_time) + '.'
                else:
                    text_to_speech += lessons[i].name + ' в ' + get_time(lessons[i].start_time) + ', '

    #обработка text
    if number_of_lessons == 0:
        text = text_to_speech
    else:
        for lesson in lessons:
            text += get_time(lesson.start_time) + '-' + get_time(lesson.end_time) + ' -- ' + lesson.name + ' -- ' + \
                   lesson.type + ' -- ' + lesson.teacher + '\n'
    return text, text_to_speech



def get_time(date):
    hours = str(date.hour)
    minute = str(date.minute)
    if len(minute) < 2:
        minute = '0' + minute
    return hours + ':' + minute
