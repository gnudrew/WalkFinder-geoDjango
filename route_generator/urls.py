from route_generator.views import SinglePageView
from django.urls import path

urlpatterns = [
    path('', SinglePageView.as_view(), name='route-generator'),
    path('b', ),
]