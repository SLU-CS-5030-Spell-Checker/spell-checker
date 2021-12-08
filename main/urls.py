from django.urls import path
from . import views
from . import views_irish

urlpatterns = [
		path('', views.index),
		path('', views_irish.index),
		path('spell_check_irish', views_irish.spell_check),
		path('spell_check2_irish', views_irish.spell_check2),
		path('spell_check', views.spell_check),
		path('spell_check2', views.spell_check2)
]
