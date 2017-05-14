"""
Geo-referencing GTFS with Census geographies methods

by Arnold Valdez
"""


import sys
from osgeo import ogr 
from kdtree1 import *
from kdtree2a import *
from bst import *
from point import *







def getCensusTractsGDAL(long_lat_list, shapefile_name,MaxX,MaxY,MinX,MinY ):

    """
    Geo referening using only GDAL
    Input
       long_lat_list: dictionary of stops
       shapefile_name: Census Shpaefile
       MaxX,MaxY,MinX,MinY : Extent of transit stops

       *Assumes points and shapefil are in the same datum/projection

    Output
       A dictionary of stops_ID (key) and GEOID (value)
    
    """
    
    driver = ogr.GetDriverByName("ESRI Shapefile")
    vector = driver.Open(shapefile_name, 0)
    layer = vector.GetLayer()
    c = layer.GetFeatureCount() 
    results_dict = {}
    i = 0

# Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(float(MaxX), float(MaxY))
    ring.AddPoint(float(MinX), float(MaxY))
    ring.AddPoint(float(MinX), float(MinY))
    ring.AddPoint(float(MaxX), float(MinY))
    ring.AddPoint(float(MaxX), float(MaxY))
    

# Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    for feature in layer:
        geom = feature.GetGeometryRef()
        i += 1
       
        print "{}/{}".format(i,c)
       
        extent = geom.GetEnvelope()
        
        if geom.Intersect(poly):

            for pt in long_lat_list:
                gid = pt['stop_id']
                lon = float(pt['stop_lon'])
                lat = float(pt['stop_lat'])
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(lon, lat)

                if point.Within(geom) == True:

                    feat_id = feature.GetField("GEOID")

                    results_dict[gid] = feat_id
    
    for pt in long_lat_list:
        gid = pt['stop_id']
        lon = pt['stop_lon']
        lat = pt['stop_lat']
        if gid not in results_dict:
            results_dict[gid] = 'NA'
    return results_dict









def RangeQuerying(long_lat_list, shapefile_name,MaxX,MaxY,MinX,MinY ):

    """
    Geo referening using range querying and GDAL
    Input
       long_lat_list: dictionary of stops
       shapefile_name: Census Shpaefile
       MaxX,MaxY,MinX,MinY : Extent of transit stops
    Output
       A dictionary of stops_ID (key) and GEOID (value)
    """

    
    driver = ogr.GetDriverByName("ESRI Shapefile")
    vector = driver.Open(shapefile_name, 0)
    layer = vector.GetLayer()
    c = layer.GetFeatureCount() 
    results_dict = {}
    i = 0

# Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(float(MaxX), float(MaxY))
    ring.AddPoint(float(MinX), float(MaxY))
    ring.AddPoint(float(MinX), float(MinY))
    ring.AddPoint(float(MaxX), float(MinY))
    ring.AddPoint(float(MaxX), float(MaxY))
    

# Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)


# Create Tree
    points = [Point(float(d['stop_lon']), float(d['stop_lat']),d['stop_id']) for d in long_lat_list]
    t1 = kdtree2(points)
   
    
    for feature in layer:
        geom = feature.GetGeometryRef()
        i += 1
       
        if i%200 == 0:
            g = float("{0:.0f}".format((float(i)/c)*100))
            print "{}% Complete, please wait...".format(g)
       
        extent = geom.GetEnvelope()
        rect = [[extent[0],extent[1]],[extent[2],extent[3]]]
        if geom.Intersect(poly):

            found = []

        
            range_query_orthogonal(t1, rect, found)

            for pt in found:
                gid = pt.key
                lon = float(pt.x)
                lat = float(pt.y)
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(lon, lat)


                
                if point.Within(geom) == True:

                    feat_id = feature.GetField("GEOID")

                    results_dict[gid] = feat_id

    for pt in long_lat_list:
        gid = pt['stop_id']
        lon = pt['stop_lon']
        lat = pt['stop_lat']
        if gid not in results_dict:
            results_dict[gid] = 'NA'
    return results_dict


    
        

def CheckStop(x,y):

    """
    Geo referening using Census API
    Input
       x,y: Lon,Lat of point
       shapefile_name: Census Shpaefile
       MaxX,MaxY,MinX,MinY : Extent of transit stops
    Output:
       A GEOID value
    """


    base = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={}&y={}&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&layers=14&format=json'.format(x,y)
    full_url = base
    js = urllib2.urlopen(base)
    data = json.load(js)

    GEOID = data['result']['geographies']['Census Blocks'][0]['GEOID']
    
    
    print GEOID







  

            


