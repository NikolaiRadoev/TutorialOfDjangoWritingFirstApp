from django.urls import path
from . import views

# 2
"""urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]"""
"""urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<int:pk>/home/', views.HomeView.as_view(), name='home'),
]"""
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/<int:user_id>', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/<int:user_id>', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    #  path('<int:pk>/home/', views.HomeView.as_view(), name='home'),
    path('<int:user_id>/home/', views.home, name='home'),
    path('create/<int:user_id>/', views.create, name='create'),
    path('<int:user_id>/result/<int:question_id>/', views.result, name='result'),
    path('<int:user_id>/logout/', views.logout, name='logout'),
]
