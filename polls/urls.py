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
    path("", views.IndexView.as_view(), name="index"),
    path("detail/question/<int:question_id>/", views.detail, name="detail"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("create/new/question/", views.create, name="create"),
    path("edit/questions/<int:question_id>/", views.edit, name="edit"),
    path("edit/questions/", views.my_questions, name="my_questions"),
    path("delete/questions/", views.my_questions_for_delete, name="my_questions_for_delete"),
    path("delete/questions/<int:question_id>/", views.delete, name="delete"),
    path("results/question/<int:question_id>/", views.results, name="results"),
    path("logout/", views.logout, name="logout"),
]
