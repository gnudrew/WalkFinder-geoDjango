# WalkFinder-geoDjango

## Concept:
Determine walking routes from arbitrary start location that are (a) time-constrained, and (b) novel experiences.
>Me: "Hey Siri, find me a 10 minute walk from here that I haven't tried before."<br>
>Siri: "Sorry, I can't do that..."<br>
>Me: "Ok. I'll make an app."<br>

## Stack:
* **Frontend**: HTML, JS, Bulma
* **Backend**: GeoDjango, OSMnx, Networkx, folium
* **Database**: PostgreSQL/PostGIS

## Installation:
* Install miniconda (or Anaconda).
* > conda config --prepend channels conda-forge 
* > conda create -n ox --strict-channel-priority osmnx
* > activate ox
* > pip install -r requirements.txt
* Add the following code to `settings.py` in the Django project, of course tweaked to use the correct path and GDAL version, which here is `gdal303.dll`:
```
os.environ['GDAL_DATA'] = r"C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo\data\gdal"
os.environ['PROJ_LIB'] = r"C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo\data\proj"
os.environ['PATH'] = r"C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo" +";" + os.environ['PATH']
GDAL_LIBRARY_PATH = r'C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo\gdal303.dll' 
```

## Usage:
* Live deployment: [WalkFinder v.0.1](https://calm-falls-98051.herokuapp.com/)
* Use it on-the-fly from your GPS-enabled mobile device from anywhere.
* Use it from your desktop browser to explore walking options branching out from your home or work location.
* Stay tuned; I'm adding features and will ship them to the above website periodically.

## Feedback or suggestions:
Feel free to reach out to me via email. I'm always collecting user stories and would appreciate your response(s) to the following questions:
1. How long do you typically go for on a walk (lower and upper bounds)?
2. When you're on a walk, what is enjoyable to you?
3. When you're on a walk, what is not enjoyable to you?
4. Before a walk, what are 2 factors that discourage or prevent you from starting? 
5. Before a walk, what are 2 factors that encourage or motivate you to start?
6. Tell me about your first impression of the app. Anything confusing?
7. If you like using this type of app, what additional features do you desire?
