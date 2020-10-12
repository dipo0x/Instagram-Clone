from core import views as views
from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views

app_name = 'core'

urlpatterns = [	

	path('profile/<str:username>/', views.user_profile),

	path('journal/<str:slug>/', views.journal_detail_view, name='journal-detail'),

	path('journal/', views.journal_list_view, name='journal'),


]
