from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from . import backend


@csrf_exempt
def get_request(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        answer = backend.answer(request_json)
        if not answer:
            response = {
                    "response": {
                        "text": "Привет, студент",
                        "tts": "Привет, ст+удент!",
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
        else:
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