from datetime import datetime, timedelta
from .models import Univercity, Group, Lesson, Dates


def answer(json):
    if 'завтра' in json['request']['nlu']['tokens']:
        tomorrow_date = datetime.today() + timedelta(days=1)
        dates = Dates.objects.filter(date=tomorrow_date)
        lessons = []
        teachers = []
        for date in dates:
            lesson = date.lesson_id
            lessons.append(lesson.name)
            teachers.append(lesson.teacher)
        answer = 'Здравствуйте, у вас завтра {} пар.'.format(len(lessons))
        for i in range(len(lessons)):
            answer = answer + '{} у {}, '.format(lessons[i], teachers[i])
        return answer
    return False
