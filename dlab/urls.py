from django.urls import path
from Auth.views import UserListView, UserDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name ='users-detail'),
]
