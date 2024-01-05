from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.urls import reverse_lazy
from django import forms

from .models import Todo

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
