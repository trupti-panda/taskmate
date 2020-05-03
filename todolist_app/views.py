from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import Tasklist
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method =="POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manager=request.user
            instance.save()
        messages.success(request,('New task added!'))
        return redirect('todolist')

    else:  
        all_tasks = Tasklist.objects.filter(manager = request.user)
        paginator=Paginator(all_tasks,3)
        page=request.GET.get("pg")
        #reloading all_tasks according to paginator
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})
@login_required
def edit_task(request,task_id):
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
    if request.method =="POST":
        task = Tasklist.objects.get(pk=task_id)
        
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        form = TaskForm(request.POST or None,instance=task)
        
        if form.is_valid():
            form.save()
            messages.success(request,('Task edited!'))
        else:
            messages.error(request, form.errors)
        return redirect('todolist')

    else:  
        task_obj = Tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})
@login_required
def delete_task(request,task_id):
    task_del = Tasklist.objects.get(pk=task_id)
    if task_del.manager == request.user:
        task_del.delete()
    else:
        messages.error(request,('This Page Is Restricted !! You Are Not Allowed.'))
    return redirect('todolist')
@login_required
def complete_task(request,task_id):
    comp_task = Tasklist.objects.get(pk=task_id)
    if comp_task.manager == request.user:
        comp_task.done=True
        comp_task.save()
    else:
        messages.error(request,('This Page Is Restricted !! You Are Not Allowed.'))
    return redirect('todolist')
@login_required
def pending_task(request,task_id):
    pendi_task = Tasklist.objects.get(pk=task_id)
    if pendi_task.manager == request.user:
        pendi_task.done=False
        pendi_task.save()
    else:
        messages.error(request,('This Page Is Restricted !! You Are Not Allowed.'))
    return redirect('todolist')

def contacts(request):
    context={
        "contacts_text":"Welcome to contacts page!"
    }
    return render(request,'contacts.html',context)
def about(request):
    context={
        "about_text":"Welcome to about page!"
    }
    return render(request,'about.html',context)
def index(request):
    context={
        "index_text":"Welcome to Home!"
    }
    return render(request,'index.html',context)