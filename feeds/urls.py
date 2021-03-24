from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.posts, name='posts'),
    path('<slug:slug>.rss', views.feed, name='feed')
]