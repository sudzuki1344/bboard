from django.shortcuts import render, redirect
from hw.models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'hw/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, description=description)
        return redirect('hw:task_list')
    return render(request, 'hw/task_create.html')

def task_update(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('hw:task_list')
    return render(request, 'hw/task_update.html', {'task': task})

def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('hw:task_list')
    return render(request, 'hw/task_delete.html', {'task': task})

