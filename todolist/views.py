from django.shortcuts import render, redirect
from todolist.models import Todo
from todolist.urls import *
from todolist.forms import TodoForm


def index(request):
    todos = Todo.objects.order_by('-published')
    context = {'todos': todos}

    return render(request, 'todolist/index.html', context)

def todo_list(request):

    pass

def todo_detail():

    pass

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

def todo_delete():

    pass


