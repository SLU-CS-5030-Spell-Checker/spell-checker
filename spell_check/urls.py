"""spell_check URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from main import views
from main import views_irish
from django.urls import path, include


urlpatterns = [
	path('admin/', admin.site.urls),
    path('spell_check', views.spell_check, name='spell_check'),
    path('ajax-test-view', views.index, name='ajax-test-view'),
    path('spell_check_irish', views_irish.spell_check, name='spell_check'),
    path('ajax-test-view_irish', views_irish.index, name='ajax-test-view_irish'),
	path('', include('main.urls'))
]

