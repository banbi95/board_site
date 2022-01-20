"""board_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name='board'

urlpatterns = [
    path('', views.IndexView.as_view(),name='home'),
    # path('<int:pk>/',views.board_topics,name='board_topics'),
    path('<int:pk>/', views.TopicListView.as_view(), name='board_topics'),
    path('<int:pk>/new-topic', views.new_topic, name='new_topic'),
    path('<int:pk>/topic/<int:topic_pk>/',views.PostListView.as_view(),name='topic_posts'),
    path('<int:pk>/topic/<int:topic_pk>/reply/',views.reply_topic, name='reply_topic'),
    path('<int:pk>/topic/<int:topic_pk>/post/<int:post_pk>/',views.edit_post, name='edit_post'),

]
