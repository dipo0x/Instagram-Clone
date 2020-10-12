from django.urls import path, include
from .import views
from core import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('dashboard', views.profile, name="dashboard"),

    path('follow/<int:pk>/', views.follow_user, name='follow_user'),

    path('register', views.register, name='register'),

    path('logout', views.user_logout, name="logout"),

    path('add_post/', core_views.journal_create_view, name='add-post'),

    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
]
