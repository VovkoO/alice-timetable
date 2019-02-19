from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json



@csrf_exempt
def get_request(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
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
<<<<<<< HEAD
        return JsonResponse(response)
=======
        return JsonResponse(json.dumps(response), safe=False)
>>>>>>> e29ea9a9205eb154995fbed320f195d7cdfbbcff
    return HttpResponse('No POST in request')


def home_page(request):
    return HttpResponse('Hello')