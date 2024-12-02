from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from todolist.models import Todo
from todolist.urls import *
from todolist.forms import TodoForm


def index(request):
    todos = Todo.objects.order_by('-published')
    context = {'todos': todos}

    return render(request, 'todolist/index.html', context)

def todo_list(request):

    pass


def todo_detail(request, todo_id):
    try:
        todo = get_object_or_404(Todo, pk=todo_id)

    except todo.DoesNotExist:
        return Http404('Такое обьявлени не существует')

    context = {'todo': todo}

    return render(request, 'todolist/bb_detail.html', context)


def todo_create(request):
    if request.method == 'POST':
        todo = TodoForm(request.POST)

        if todo.is_valid():
            todo.save()
            return redirect('todolist:index')
        else:
            todo = TodoForm(request.POST)
            context = {'form': todo}
            return render(request, 'todolist/create.html', context)
    else:
        todo = TodoForm()
        context = {'form': todo}
        return render(request, 'todolist/create.html', context)


@csrf_protect
def todo_delete(request, todo_id):

    todo = get_object_or_404(Todo, pk=todo_id)

    context = {'todo': todo}

    if request.method == 'POST':

        todo.delete()

        return redirect('todolist:index')

    return render(request, 'todolist/delete.html', context)