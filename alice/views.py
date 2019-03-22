from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
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
    return render(request, 'add_timetable.html', {'user': auth.get_user(request).get_username()})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'add_timetable.html', {'user': auth.get_user(request).get_username()})
        else:
            return render(request, 'login.html', {'error': 'Нерпавильный email или пароль', 'user': auth.get_user(request).get_username()})
    return render(request, 'login.html', {'user': auth.get_user(request).get_username()})


def logout(request):
    auth.logout(request)
    return render(request, 'add_timetable.html', {'user': auth.get_user(request).get_username()})