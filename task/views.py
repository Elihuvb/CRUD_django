from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # para protegeer rutas

# Create your views here.

# Retorna la pagina principal
def hello(request):
    return render(request, "index.html")

def singup(request):
    if request.method == 'GET': # si imprime algo lo renderizo a la pagina de registro
        return render(request, "signup.html", {
            'form': UserCreationForm # imprimo un formulario vacio
        })
    else:
        if request.POST['password1'] == request.POST['password2']: # si las passwords son iguales...
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1']) # se crea el usuario
                user.save() # se guarda en una base de datos
                login(request, user) # se entra en el nuevo perfil
                return redirect("task") # se redirecciona a la pagina de "task"
            except IntegrityError: # si surge un error de integridad...
                return render(request, "signup.html", { # se retorna a la pagina de registro...
                    'form': UserCreationForm, # con un formulario nuevo...
                    'error': 'User already exists' # y un mensaje de error.
                })
        return render(request, "signup.html", {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })

@login_required
def task(request):
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=True)
    return render(request, "task.html", {
        'tasks': tasks
        }) # retorna la pagina de task

@login_required
def task_complete_list(request):
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=False).order_by('-datecomplete')
    return render(request, "task.html", {
        'tasks': tasks
        }) # retorna la pagina de task

@login_required
def new_task(request):
    
    if request.method == 'GET':
        return render(request, "new_task.html", {
            'form': TaskForm
        })
    else:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('task')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id,  user=request.user)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except:
            return render(request, "task_detail.html", {'task': task, 'form': form, 'error': 'error updating task'})

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.datecomplete = timezone.now()
        task.save()
        return redirect('task')

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

@login_required
def signout(request): # funcion para cerrar sesion sin borrarla
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == 'GET':
        return render(request, "signin.html", {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "signin.html", {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect("task")