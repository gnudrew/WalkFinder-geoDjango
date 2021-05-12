from django.shortcuts import render
from django.http import HttpResponse

import folium

# Create your views here.
def home_view(request):
    # return HttpResponse("<h1>Hello World!</h1>")
    # print(request)
    # print(render(request, "home.html"))
    return render(request, "home.html", {})

def mapgen_view(request):
    if request.method=='POST':
        target_time = request.POST.get('target_time')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        print((target_time,lat,lon))
    return render(request, "mapgen.html", {'target_time':target_time, 'lat':lat, 'lon':lon, 'folium_map':f})