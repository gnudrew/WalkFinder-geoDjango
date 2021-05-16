from django.shortcuts import render
from django.http import HttpResponse

from .buildmap import buildmap_start, buildmap_route
from random import random as r # interval r() -> x in [0,1)

# Create your views here.
def home_view(request):
    # return HttpResponse("<h1>Hello World!</h1>")
    # print(request)
    # print(render(request, "home.html"))

    # request.session['fav_color']='red'
    # print('Home_View session: fav_color is:', request.session['fav_color'])

    return render(request, "home.html", {})

def mapgen_view(request):
    if request.method=='POST':
        # get form inputs
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        # store to session
        request.session['lat'] = lat
        request.session['lon'] = lon
        # server-side print
        print('======== mapgen_view ========')
        print("(lat,lon) = ",str((lat,lon)))
        print('====== END mapgen_view ======')
        # build map
        m = buildmap_start(lat, lon)

        return render(request, "mapgen.html", {'lat':lat, 'lon':lon, 'folium_map':m._repr_html_()})
    
    if request.method=='GET':
        # Change this to URL routing: If user submits GET request manually at URL `/mapgen/` redirect to URL `/`.
        return render(request,"home.html")

def routegen_view(request):
    if request.method=='GET':
        # m is the folium map from the previous call of mapgen_view().
        # for now, I'll regenerate it with hard-coded location.
        # Later, I'll probably store either the map object, or the details needed to regenerate it in the database
        # ... like under some "Previous Map" location in memory.

        # retrieve session inputs
        lat = request.session['lat']
        lon = request.session['lon']
        # build map
        m = buildmap_start(lat,lon)

        return render(request, "routegen.html", {'folium_map':m._repr_html_()})

    if request.method=='POST':
        # get form input
        target_time = request.POST.get('target_time')
        # store to session
        request.session['target_time'] = target_time

        # m is the folium map from the previous call of mapgen_view() or routegen_view().
        # regenerate it for now with hard-coded coordinates
        # Later, I'll probably store either the map object, or the details needed to regenerate it in the database
        # ... like under some "Previous Map" location in memory.

        # retrieve map inputs from session
        lat = float(request.session['lat'])
        print('LAT is',lat,'with type',type(lat))
        lon = float(request.session['lon'])

        # randomly generate end lat and lon
        rand_lat = (lat-.01) + .02*r()
        rand_lon = (lon-.02) + .04*r()
        # store to session
        request.session['rand_lat'] = rand_lat
        request.session['rand_lon'] = rand_lon
        # build map
        m = buildmap_start(lat, lon)
        m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon))
        return render(request, "routegen.html", {'target_time':target_time, 'folium_map':m._repr_html_() })

def walk_view(request):
    # retrieve map inputs from session
    lat = float(request.session['lat'])
    lon = float(request.session['lon'])
    rand_lat = float(request.session['rand_lat'])
    rand_lon = float(request.session['rand_lon'])
    target_time = int(request.session['target_time'])

    m = buildmap_start(lat, lon)
    m = buildmap_route(m, target_time, (lat, lon), (rand_lat, rand_lon))
    
    return render(request, "walk.html", {'folium_map':m._repr_html_() })