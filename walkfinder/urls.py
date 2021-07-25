"""walkfinder URL Configuration

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
from django.urls import path
from routes.views import home_view, mapgen_view, routegen_view, walk_view
from django.views.generic.base import RedirectView

from routes.views import SinglePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('mapgen/', mapgen_view),
    path('routegen/', routegen_view),
    path('walk/', walk_view),
    path('spa', SinglePageView.as_view(), name='single-page-view'),
    # path('favicon.ico', RedirectView.as_view(url='favicon.svg'))
]   