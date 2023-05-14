from django.urls import path
from .views import RegisterView, LoginView, DeleteView, UserListView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('delete/<int:user_id>', DeleteView.as_view()),
    path('list', UserListView.as_view())
]
