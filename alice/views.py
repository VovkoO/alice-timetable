from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .models import SiteUsers, Group, Lesson, User, Univercity, Admin
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
            ##Если пользователь уже выбрал расписание
            user = SiteUsers.objects.get(user_id=auth.get_user(request))
            group = user.group_id
            try:
                Admin.objects.get(user_id=auth.get_user(request), group_id=group)
                admin = True
            except Admin.DoesNotExist:
                admin = False
            lessons = Lesson.objects.filter(group_id=group)
            mon = lessons.filter(day_of_week=0)
            tue = lessons.filter(day_of_week=1)
            wed = lessons.filter(day_of_week=2)
            thu = lessons.filter(day_of_week=3)
            fri = lessons.filter(day_of_week=4)
            sat = lessons.filter(day_of_week=5)
            sun = lessons.filter(day_of_week=6)
            tomorrow = site_backend.get_tomorrow_lessons(SiteUsers.objects.get(user_id=auth.get_user(request)).group_id)

            admin_message = ''
            if request.method == 'POST':

                ##Выбрать другое расписание
                if 'change_timetable' in request.POST:
                    user.delete()
                    return redirect('timetable')

                ##Добавление нового админа
                if 'add_admin' in request.POST:
                    email = request.POST.get('email')
                    try:
                        new_admin = User.objects.get(email=email)
                        try:
                            new_admin = Admin.objects.get(user_id=new_admin, group_id=group)
                            admin_message = email + ' уже является админом.'
                        except Admin.DoesNotExist:
                            Admin.objects.create(user_id=new_admin, group_id=group)
                            admin_message = email + ' теперь является админом.'
                    except User.DoesNotExist:
                        admin_message = 'Такого пользователя не существует.'

            response = {
                'user': auth.get_user(request),
                'admin': admin,
                'group': group.name,
                'admin_message': admin_message,
                'mon': mon,
                'mon1_len': len(mon.filter(repeat=0)) + len(mon.filter(repeat=1)) > 0,
                'mon2_len': len(mon.filter(repeat=0)) + len(mon.filter(repeat=2)) > 0,
                'tue': tue,
                'tue1_len': len(tue.filter(repeat=0)) + len(tue.filter(repeat=1)) > 0,
                'tue2_len': len(tue.filter(repeat=0)) + len(tue.filter(repeat=2)) > 0,
                'wed': wed,
                'wed1_len': len(wed.filter(repeat=0)) + len(wed.filter(repeat=1)) > 0,
                'wed2_len': len(wed.filter(repeat=0)) + len(wed.filter(repeat=2)) > 0,
                'thu': thu,
                'thu1_len': len(thu.filter(repeat=0)) + len(thu.filter(repeat=1)) > 0,
                'thu2_len': len(thu.filter(repeat=0)) + len(thu.filter(repeat=2)) > 0,
                'fri': fri,
                'fri1_len': len(fri.filter(repeat=0)) + len(fri.filter(repeat=1)) > 0,
                'fri2_len': len(fri.filter(repeat=0)) + len(fri.filter(repeat=2)) > 0,
                'sat': sat,
                'sat1_len': len(sat.filter(repeat=0)) + len(sat.filter(repeat=1)) > 0,
                'sat2_len': len(sat.filter(repeat=0)) + len(sat.filter(repeat=2)) > 0,
                'sun': sun,
                'sun1_len': len(sun.filter(repeat=0)) + len(sun.filter(repeat=1)) > 0,
                'sun2_len': len(sun.filter(repeat=0)) + len(sun.filter(repeat=2)) > 0,
                'tomorrow': tomorrow,
                'tomorrow_len': len(tomorrow) > 0
            }

            return render(request, 'timetable.html', response)

        except SiteUsers.DoesNotExist:
            if request.method == 'POST':
                ##Если посльзователь выбирает расписание
                if 'choose_timetable' in request.POST:
                    univercity_input = request.POST.get('univercity')
                    try:
                        univercity = Univercity.objects.get(name=univercity_input)
                    except Univercity.DoesNotExist:
                        try:
                            readable_univercity_input = univercity_input.lower().replace(' ', '').replace('-', '')
                            univercity = Univercity.objects.get(readable_name=readable_univercity_input)
                        except Univercity.DoesNotExist:
                            return render(request, 'timetable.html', {'does_not_exist': 'Для такого ВУЗа нет расписания',
                                                                      'user': auth.get_user(request),
                                                                      'site_user_does_not_exist': '-'})
                    try:
                        group_input = request.POST.get('group')
                        group = Group.objects.get(univerсity_id=univercity, name=group_input)
                        SiteUsers.objects.create(user_id=auth.get_user(request), univerсity_id=univercity,
                                                 group_id=group)
                        return redirect('timetable')
                    except Group.DoesNotExist:
                        readable_group_input = group_input.lower().replace(' ', '').replace('-', '')
                        try:
                            group = Group.objects.get(univerсity_id=univercity, readable_name=readable_group_input)
                            SiteUsers.objects.create(user_id=auth.get_user(request), univerсity_id=univercity,
                                                     group_id=group)
                            return redirect('timetable')
                        except Group.DoesNotExist:
                            return render(request, 'timetable.html', {'does_not_exist': 'Для такой группы нет расписания',
                                                                      'user': auth.get_user(request),
                                                                      'site_user_does_not_exist': '-'})
                ##Если пользователь добавляет новое расписание
                elif 'add_timetable' in request.POST:
                    univercity = request.POST.get('univercity')
                    group = request.POST.get('group')
                    start_date = request.POST.get('start_date')
                    end_date = request.POST.get('end_date')
                    user = auth.get_user(request)
                    message = site_backend.add_timetable(univercity, group, start_date, end_date, user)
                    return render(request, 'timetable.html', {'user': user, 'message': message})
            return render(request, 'timetable.html', {'user': auth.get_user(request),
                                                      'site_user_does_not_exist': 'У вас нет расписания, создайте его, либо, попросите '
                                                                                  'доступ к нему у другого человека, который его создал'})
    return render(request, 'timetable.html', {'user': auth.get_user(request)})


def change_lesson(request):
    if request.method == 'POST':
        message = ''
        print(request.POST.get('lesson_id'))
        lesson = Lesson.objects.get(pk=request.POST.get('lesson_id'))
        if 'change_lesson' in request.POST:
            name = request.POST.get('lesson')
            teacher = request.POST.get('teacher')
            classroom = request.POST.get('classroom')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            type = request.POST.get('type')
            day_of_week = int(request.POST.get('day_of_week'))
            repeat = int(request.POST.get('repeat'))
            user = SiteUsers.objects.get(user_id=auth.get_user(request))
            start_date = user.group_id.start_date
            end_date = user.group_id.end_date
            message = site_backend.change_lesson(lesson, name, teacher, classroom, start_time, end_time, type,
                                                 day_of_week, repeat, start_date, end_date)
        lesson = Lesson.objects.get(pk=request.POST.get('lesson_id'))
        start_time = str(lesson.start_time)
        end_time = str(lesson.end_time)
        user = auth.get_user(request)
        group = SiteUsers.objects.get(user_id=user).group_id
        try:
            Admin.objects.get(user_id=user, group_id=group)
            admin = True
        except Admin.DoesNotExist:
            admin = False
            message = 'Для того, что бы делать изменения, попросите разрешение у админа'
        response = {
            'admin': admin,
            'lesson': lesson,
            'start_time': start_time[0:len(start_time)-3],
            'end_time': end_time[0:len(end_time)-3],
            'user': auth.get_user(request),
            'message': message
        }
    return render(request, 'change_lesson.html', response)


def add_timetable(request):
    # if request.method == 'POST':
    #     group_name = request.POST.get('group')
    #     lesson = request.POST.get('lesson')
    #     teacher = request.POST.get('teacher')
    #     classroom = request.POST.get('classroom')
    #     start_time = request.POST.get('start_time')
    #     end_time = request.POST.get('end_time')
    #     day_of_week = request.POST.get('day_of_week')
    #     start_date = request.POST.get('start_date')
    #     end_date = request.POST.get('end_date')
    #     repeat = request.POST.get('repeat')
    #     success = site_backend.add_lesson(group_name, lesson, teacher, classroom, start_time, end_time, day_of_week,
    #                                       start_date, end_date, repeat)
    #     if success:
    #         return render(request, 'add_timetable.html', {'if_add': 'Предмет добавлен'})
    #     else:
    #         return render(request, 'add_timetable.html', {'if_add': 'Даты не добавлены'})
    return render(request, 'add_timetable.html', {'user': auth.get_user(request)})


def add_lesson(request):
    if request.method == 'POST':
        user = SiteUsers.objects.get(user_id=auth.get_user(request))
        group_name = user.group_id
        lesson = request.POST.get('lesson')
        teacher = request.POST.get('teacher')
        classroom = request.POST.get('classroom')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        start_date = user.group_id.start_date
        end_date = user.group_id.end_date
        day_of_week = request.POST.get('day_of_week')
        repeat = request.POST.get('repeat')
        type = request.POST.get('type')
        success = site_backend.add_lesson(group_name, lesson, teacher, classroom, start_time, end_time,
                                          day_of_week, repeat, type, start_date, end_date)
        return render(request, 'add_lesson.html', {'message': success, 'user': auth.get_user(request)})
    return render(request, 'add_lesson.html', {'user': auth.get_user(request)})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('timetable')
        else:
            return render(request, 'login.html', {'error': 'Нерпавильный email или пароль', 'user': auth.get_user(request)})
    return render(request, 'login.html', {'user': auth.get_user(request)})


def register(request):
    if request.method == 'POST':
        input_username = request.POST.get('email')
        input_password = request.POST.get('password')
        try:
            User.objects.get(username=input_username)
            return render(request, 'register.html', {'error': 'Пользователь с таким email уже существует', 'user': auth.get_user(request)})
        except User.DoesNotExist:
            user = User.objects.create(username=input_username, password=input_password)
            user.set_password(input_password)
            user.save()
            user = auth.authenticate(username=input_username, password=input_password)
            auth.login(request, user)
            return redirect('timetable')
    return render(request, 'register.html', {'user': auth.get_user(request)})


def logout(request):
    auth.logout(request)
    return redirect('timetable')