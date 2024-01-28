from django.urls import path

from . import views

app_name = "TO_DO"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.UpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.DeleteTodoView.as_view(), name="Todo_delete"),
]

urlpatterns += [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
