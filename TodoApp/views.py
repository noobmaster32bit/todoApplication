from django.shortcuts import render,redirect
from django.views.generic import View
from TodoApp.models import Task
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=("created_date",)

# View for listing all tasks
# url : localhost:8000/tasks/all/
# methods : get
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Task.objects.all()
        return render(request,"task_list.html",{"data":qs})

# View for adding tasks
# url : localhost:8000/tasks/add/
# methods : get,post  
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)
            return redirect("task-list")
        else:
            return render(request,"task_add.html",{"form":form})

# View for task detail
# url : localhost:8000/tasks/{pk}/
# methods : get 
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        return render(request,"task_detail.html",{"data":qs})


# View for deleting task
# url : localhost:8000/tasks/{pk}/remove
# methods : get    
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.filter(id=id).delete()
        return redirect("task-list")
    
# View for task editing
# url : localhost:8000/tasks/{pk}/change
# methods : get,post

class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(instance=task_object)
        return render(request,"task_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(request.POST,instance=task_object)
        if form.is_valid():
            form.save()
            return redirect("task-list")    
        else:
            return render(request,"task_edit.html",{"form":form})
        



        


    