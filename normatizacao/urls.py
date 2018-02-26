from django.urls import path
from . import views
app_name = 'normatizacao'
urlpatterns=[
    path('', views.NormatizadorList.as_view()),
]