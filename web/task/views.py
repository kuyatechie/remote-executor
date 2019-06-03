from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser

from task.models import Task
from task.serializers import TaskSerializer, TaskObjectsSerializer
from task.lib.message import MessageGenerator, Messenger

import uuid
import ast
from datetime import datetime

messenger = Messenger()


def index(request):
    return HttpResponse("Hello, world")


@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data["created"] = datetime.today()
        data["uid"] = uuid.uuid1()
        data["uid"] = uuid.uuid1()
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = MessageGenerator(uid=data["uid"], script=data["script"], arguments=data["arguments"])
            messenger.submit(message.generate_message())
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'GET':
        return HttpResponse(status=405)


@csrf_exempt
def view_pk(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.arguments = ast.literal_eval(task.arguments)
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)


@csrf_exempt
def view_uid(request, uid):
    try:
        task = Task.objects.get(uid=uid)
        task.arguments = ast.literal_eval(task.arguments)
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    except ValidationError as e:
        return HttpResponse(e, status=400)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)


@csrf_exempt
def view_day_tasks(request, date):
    try:
        if date == "today":
            today = datetime.today()
            date = "{}{}{}".format(today.year, today.month, today.day)
        task = Task.objects.filter(created__date=datetime.strptime(date, '%Y%m%d').date())
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    except ValueError:
        return HttpResponse("Invalid date. Use YYYMMDD.", status=400)

    if request.method == 'GET':
        serializer = TaskObjectsSerializer(task, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def view_day_tasks_count(request, date):
    try:
        if date == "today":
            today = datetime.today()
            date = "{}{}{}".format(today.year, today.month, today.day)
        task_count = Task.objects.filter(created__date=datetime.strptime(date, '%Y%m%d').date()).count()
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    except ValueError:
        return HttpResponse("Invalid date. Use YYYMMDD.", status=400)

    if request.method == 'GET':
        return JsonResponse(task_count, safe=False)
