from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# --- Endpoints for Task List ---

@api_view(['GET', 'POST'])
def tasks_list(request):
    """
    List all tasks or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    """
    Retrieve, update, or delete a task.
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Endpoint to return a list (array) of users ---

@api_view(['GET'])
def users_list(request):
    """
    Return a list of all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data) 