from django.urls import path

from . import views


app_name='tags'
urlpatterns = [
    path('', views.index, name='index'),
    path('all_tags', views.all_tags, name='all_tags'),
]