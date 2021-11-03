from django.urls import path
from . import views

urlpatterns = [
		path('', views.index),
		path('spell_check', views.spell_check)
]
