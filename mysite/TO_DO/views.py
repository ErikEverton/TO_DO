from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import auth, User   
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms

from .models import Todo
from .forms import CreateUserForm, LoginForm

# Create your views here.

@method_decorator(login_required(login_url='TO_DO:login'), name='dispatch')
class IndexView(generic.ListView):
    template_name = "TO_DO/index.html"
    context_object_name = "to_do_list"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        queryset = Todo.objects.filter(user=user)
        return queryset.order_by("-date")


@method_decorator(login_required(login_url='TO_DO:login'), name='dispatch')
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


@method_decorator(login_required(login_url='TO_DO:login'), name='dispatch')
class CreateView(generic.CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "TO_DO/create.html"
    success_url = reverse_lazy("TO_DO:index")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='TO_DO:login'), name='dispatch')
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
            return redirect("TO_DO:login")
    
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

                return redirect('TO_DO:index')
    
    context = {'loginform': form}
    return render(request, 'TO_DO/Auth/login.html', context=context)


def user_logout(request):
    logout(request)

    return redirect('TO_DO:login')
