from django.shortcuts import render,redirect
from django.views.generic import View
from TodoApp.models import Task
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["email","username","password"]
    
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=("created_date","user_object")

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

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
            # form.save()
            data=form.cleaned_data
            Task.objects.create(**data,user_object=request.user)
            # print(request.POST)
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
        
# Signup view
# url : localhost:8000/signup
# methods : get,post

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("userdata created")
            return redirect("signin")
        else:
            print("failed to created userdata")
        return render(request,"register.html",{"form":form})
    
# Signin View
# url : localhost:8000/signin
# methods : get,post
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                print("user credentials correct")
                return redirect("task-list")
        print("invalid credentials")
        return render(request,"login.html",{"form":form})

# SignOut View
# url : localhost:8000/signout
# methods : get

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")






        


    