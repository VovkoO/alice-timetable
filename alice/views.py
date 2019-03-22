from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .models import SiteUsers, Group, Lesson
import json
from . import site_backend, alice_backend


@csrf_exempt
def get_request(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        answer = alice_backend.get_answer(request_json)
        answer = str(answer)
        response = {
            "response": {
                "text": answer,
                "tts": answer,
                "end_session": False
            },
            "session": {
                "session_id": request_json['session']['session_id'],
                "message_id": request_json['session']['message_id'],
                "user_id": request_json['session']['user_id']
            },
            "version": "1.0"
        }
        return JsonResponse(response)
    return HttpResponse('No POST in request')


def home_page(request):
    return HttpResponse('Hello')


def timetable(request):
    if auth.get_user(request).is_authenticated:
        try:
            user = SiteUsers.objects.get(user_id=auth.get_user(request))
            group = user.group_id
            lessons = Lesson.objects.filter(group_id=group)
            mon = lessons.filter(day_of_week=0)
            tue = lessons.filter(day_of_week=1)
            wed = lessons.filter(day_of_week=2)
            thu = lessons.filter(day_of_week=3)
            fri = lessons.filter(day_of_week=4)
            sat = lessons.filter(day_of_week=5)
            sun = lessons.filter(day_of_week=6)

            response = {
                'user': auth.get_user(request),
                'mon': mon,
                'mon_len': len(mon) > 0,
                'tue': tue,
                'tue_len': len(tue) > 0,
                'wed': wed,
                'wed_len': len(wed) > 0,
                'thu': thu,
                'thu_len': len(thu) > 0,
                'fri': fri,
                'fri_len': len(fri) > 0,
                'sat': sat,
                'sat_len': len(sat) > 0,
                'sun': sun,
                'sun_len': len(sun) > 0
            }
            return render(request, 'timetable.html', response)

        except SiteUsers.DoesNotExist:
            return render(request, 'timetable.html', {'user': auth.get_user(request), 'error': 'У вас нет расписания, создайте его, либо, попросите '
                                                               'доступ к нему у другого человека, который его создал'})
    return render(request, 'timetable.html', {'user': auth.get_user(request)})


def add_timetable(request):
    if request.method == 'POST':
        univercity_name = request.POST.get('univercity')
        group_name = request.POST.get('group')
        lesson = request.POST.get('lesson')
        teacher = request.POST.get('teacher')
        classroom = request.POST.get('classroom')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        day_of_week = request.POST.get('day_of_week')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        repeat = request.POST.get('repeat')
        success = site_backend.add_to_db(univercity_name, group_name, lesson, teacher, classroom, start_time, end_time, day_of_week,
                                         start_date, end_date, repeat)
        if success:
            return render(request, 'add_timetable.html', {'if_add': 'Предмет добавлен'})
        else:
            return render(request, 'add_timetable.html', {'if_add': 'Даты не добавлены'})
    return render(request, 'add_timetable.html', {'user': auth.get_user(request)})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'add_timetable.html', {'user': auth.get_user(request)})
        else:
            return render(request, 'login.html', {'error': 'Нерпавильный email или пароль', 'user': auth.get_user(request)})
    return render(request, 'login.html', {'user': auth.get_user(request)})


def logout(request):
    auth.logout(request)
    return render(request, 'add_timetable.html', {'user': auth.get_user(request)})