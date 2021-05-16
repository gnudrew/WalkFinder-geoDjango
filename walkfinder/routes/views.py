from django.shortcuts import render
from django.http import HttpResponse

from .buildmap import buildmap_start, buildmap_route

# Create your views here.
def home_view(request):
    # return HttpResponse("<h1>Hello World!</h1>")
    # print(request)
    # print(render(request, "home.html"))
    request.session['fav_color']='red'
    print('Home_View session: fav_color is:', request.session['fav_color'])
    return render(request, "home.html", {})

def mapgen_view(request):
    if request.method=='POST':
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        print('======== mapgen_view ========')
        print((lat,lon))

        m = buildmap_start(lat, lon)

        print('~~~ BEGIN SESSION TEST ~~~')
        fav_color = request.session['fav_color']
        print('fav_color is:',fav_color)
        print('Setting fav_color to blue...')
        request.session['fav_color'] = 'blue'
        if request.session['fav_color'] == 'blue':
            print('SUCCESS: new fav_color is blue')
        else:
            print('FAILURE: new fav_color not blue')
        print('~~~ END OF SESSION TEST ~~~')

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
        m = buildmap_start(44.784878,-93.143651)

        return render(request, "routegen.html", {'folium_map':m._repr_html_()})

    if request.method=='POST':
        target_time = request.POST.get('target_time')
        # m is the folium map from the previous call of mapgen_view() or routegen_view().
        # regenerate it for now with hard-coded coordinates
        # Later, I'll probably store either the map object, or the details needed to regenerate it in the database
        # ... like under some "Previous Map" location in memory.

        tmp_lat = 44.784878
        tmp_lon = -93.143651

        m = buildmap_start(tmp_lat, tmp_lon)
        m = buildmap_route(m, target_time, (tmp_lat, tmp_lon))
        return render(request, "routegen.html", {'target_time':target_time, 'folium_map':m._repr_html_() })

def walk_view(request):
    tmp_lat = 44.784878
    tmp_lon = -93.143651

    m = buildmap_start(tmp_lat, tmp_lon)
    m = buildmap_route(m, 10, (tmp_lat, tmp_lon))
    
    return render(request, "walk.html", {'folium_map':m._repr_html_() })