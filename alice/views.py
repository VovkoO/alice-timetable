from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json



@csrf_exempt
def get_request(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        return HttpResponse(str(request_json))
    return HttpResponse('No POST in request')


def home_page(request):
    return HttpResponse('Hello')