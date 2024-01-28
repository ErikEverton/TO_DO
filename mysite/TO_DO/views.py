from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django import forms

from .models import Todo
from .forms import CreateUserForm, LoginForm

# Create your views here.

class IndexView(generic.ListView):
    template_name = "TO_DO/index.html"
    context_object_name = "to_do_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Todo.objects.order_by("-date")


class DeleteTodoView(generic.DeleteView):
    model = Todo
    template_name = "TO_DO/confirm_delete.html"
    success_url = reverse_lazy("TO_DO:index")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "date"]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CreateView(generic.CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "TO_DO/create.html"
    success_url = reverse_lazy("TO_DO:index")


class UpdateView(generic.UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "TO_DO/update.html"
    success_url = reverse_lazy("TO_DO:index")


#Authentication and login
    
def registerUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("")
    
    context = {'registerform': form}

    return render(request, 'TO_DO/Auth/register.html', context=context)
        

def loginUser(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect('')
    
    context = {'loginform': form}
    return render(request, 'TO_DO/Auth/login.html', context=context)
