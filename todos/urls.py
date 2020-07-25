from django.urls import path

from todos import views

urlpatterns = [
    path('todos/', views.todo_list),
    path('todo/<slug:todo_id>', views.todo_detail),
]
