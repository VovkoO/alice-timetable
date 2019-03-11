from datetime import timedelta, datetime


def get_answer(json_request):
    date = get_date(json_request)
    print(date)
    # if date is None:
    #     return 'Извините, я не поняла, на какую дату вы бы хотели узнать расписание?'
    # return False
    return date


def get_date(json_request):
    timezone = json_request['meta']['timezone']
    today = datetime.now()
    date_dict = None
    for token in json_request['request']['nlu']['entities']:
        if 'type' in token and token['type'] == 'YANDEX.DATETIME':
            print('нашел YANDEX.DATETIME')
            date_dict = token['value']
            break
    if date_dict is None:   ##Обрабатываем дни недели
        print('Обрабатываем дни недели')
        words = json_request['request']['nlu']['tokens']
        day_of_week = get_day_of_week(json_request['request']['nlu']['tokens'])
        today_week_day = datetime.weekday(today)
        if day_of_week is not None:
            print('Нашли день недели')
            print(str(day_of_week))
            if ('предыдущий' or 'предыдущая' or 'предыдущую' or 'прошлый' or 'прошлая' or 'прошлую') in words:
                if day_of_week == today_week_day:
                    return today - timedelta(7)
                if today_week_day > day_of_week:
                    return today - timedelta(today_week_day - (today_week_day - day_of_week))
                if today_week_day < day_of_week:
                    return today - timedelta(7 - (day_of_week - today_week_day))
            else:
                if day_of_week == today_week_day:
                    return today + timedelta(7)
                if today_week_day > day_of_week:
                    return today + timedelta(7 - today_week_day + day_of_week)
                if today_week_day < day_of_week:
                    return today - timedelta(day_of_week - today_week_day)


    else:   ##Если в запросе уже есть данные о дате
        print('обрабатываем дату yandex ditetime')

        if 'year_is_relative' in date_dict:
            if date_dict['year_is_relative']:
                return today + timedelta(year=date_dict['year'])
            else:
                year = int(date_dict['year'])
        else:
            year = today.year

        if 'month_is_relative' in date_dict:
            if date_dict['month_is_relative']:
                return today + timedelta(month=date_dict['month'])
            else:
                month = int(date_dict['month'])
        else:
            month = today.month

        if 'day_is_relative' in date_dict:
            if date_dict['day_is_relative']:
                return today + timedelta(date_dict['day'])
            else:
                day = date_dict['day']
        else:
            day = today.day
        return datetime(day, month, year)

    if ('расписание' or 'пары') in json_request['request']['nlu']['tokens']:
        return datetime.now()

    return None


def get_day_of_week(words):
    print(words)
    if 'понедельник' in words:
        return 0
    if 'вторник' in words:
        return 1
    if ('среда' or 'среду') in words:
        print('среда')
        return 2
    if 'четверг' in words:
        return 3
    if ('пятница' or 'пятницу') in words:
        return 4
    if ('суббота' or 'субботу') in words:
        return 5
    if 'воскресенье' in words:
        return 6
    return None
