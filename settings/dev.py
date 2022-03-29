"""
Development-specific Settings.

To use me, set the environment variable: 
DJANGO_SETTINGS_MODULE = settings.dev
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

OSGEO4W = r"C:\OSGeo4W"
os.environ['OSGEO4W_ROOT'] = OSGEO4W
os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
GDAL_LIBRARY_PATH = OSGEO4W + r"\bin\gdal304.dll"

## OR 

# os.environ['GDAL_DATA'] = r"C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo\data\gdal"
# os.environ['PROJ_LIB'] = r"C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo\data\proj"
# os.environ['PATH'] = r"C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo" +";" + os.environ['PATH']
# GDAL_LIBRARY_PATH = r'C:\Users\gnudr\miniconda3\envs\ox\Lib\site-packages\osgeo\gdal303.dll' 
# GDAL_LIBRARY_PATH = 'C:\OSGeo4W64\share\gdal'
