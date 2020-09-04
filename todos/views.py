
from datetime import timedelta

import pytz
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from todos.models import Todo
from todos.serializers import TodoSerializer
from utils.getStatus import getStatus
from utils.getTimedeltaSec import getTimedeltaSec


@api_view(['GET', 'POST', 'DELETE'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()

        response_data = []
        for todo in todos:
            ddl = (todo.deadline.astimezone(pytz.timezone('Asia/Taipei')) +
                   timedelta(hours=8)).astimezone(pytz.timezone('Asia/Taipei'))

            ddl_string = ddl.strftime("%Y/%m/%d %H:%M")

            response_data.append(
                dict(id=str(todo.id), title=todo.title,
                     ddl=ddl_string, status=getStatus(todo)
                     ))

        response_data.sort(key=getTimedeltaSec, reverse=True)

        return JsonResponse(response_data, safe=False)

    if request.method == 'POST':
        todo_data = JSONParser().parse(request)
        todo_serializer = TodoSerializer(data=todo_data)
        if todo_serializer.is_valid():
            todo_serializer.save()
            return JsonResponse(todo_serializer.data,
                                status=status.HTTP_201_CREATED)

        return JsonResponse(todo_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        count = Todo.objects.all().delete()
        return JsonResponse(
            {'message': '{} Todos were deleted successfully!'.format(count)},
            status=status.HTTP_204_NO_CONTENT
        )

    return JsonResponse(
        {'message': 'Unhandled Request'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return JsonResponse(
            {'message': 'The todo does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        todo_serializer = TodoSerializer(todo)
        return JsonResponse(todo_serializer.data)

    if request.method == 'PUT':
        todo_data = JSONParser().parse(request)
        todo_serializer = TodoSerializer(todo, data=todo_data)
        if todo_serializer.is_valid():
            todo_serializer.save()
            return JsonResponse(todo_serializer.data)

        return JsonResponse(todo_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        todo.delete()
        return JsonResponse(
            {'message': 'Tutorial was deleted successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )

    return JsonResponse(
        {'message': 'Unhandled Request'},
        status=status.HTTP_400_BAD_REQUEST
    )
