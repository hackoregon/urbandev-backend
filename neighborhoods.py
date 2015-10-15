# Standard python imports
import os, sys

# Web app imports
from flask import jsonify, request, Response

import geojson
import shapely.wkt

# Our utilities & libs
import consts
from util import genMarkdownResult, getDbConn, geoJSONBuildFeatureCollection


   
def neighborhoods_api():
    if len(request.args) == 0:
        return genMarkdownResult('doc/neighborhoods.md')   
   
    nbrhoods = request.args.get('name')
    bounds = request.args.get('bounds') 
    option = request.args.get('option')
    
    if bounds:
        try:
            # bounds is x1, y1, x2, y2
            ext = [float(pt) for pt in bounds.split(',')]
        except ValueError:
            return 'Error: Bounds values must be floats'
    else:
        # Use the default BBX of the entire city
        ext = consts.PDX_BOUNDING_BOX

    # POLYGON(x1 y1, x1 y2, x2 y2, x2 y1, x1 y1)
    mbrPolyWKT = "'POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))'" % (ext[0], ext[1], ext[0], \
                 ext[3], ext[2], ext[3], ext[2], ext[1], ext[0], ext[1])
                 
   
    # Base sql
    sql = "SELECT id, name, AsText(shape) FROM neighborhoods2 "
    
    if option == 'intersects':
        # Grab any neighborhood polygon whose bbx intersects the viewport 
        sql += "WHERE MbrContains(PolygonFromText({0}), shape) " \
               "OR MbrIntersects(PolygonFromText({0}), shape)".format(mbrPolyWKT)

    elif option == 'contains':
        # Grab only neighborhood polygons whose bbx is completely within the viewport 
        sql += "WHERE MbrContains(PolygonFromText({0}), shape)".format(mbrPolyWKT)

    qParams = []
    if nbrhoods:
        nbrs = nbrhoods.split(',')
        if 'WHERE' in sql:
            sql += " AND name IN (" + "%s," * len(nbrs)
        else:
            sql += " WHERE name IN (" + "%s," * len(nbrs)
        sql = sql[:-1] + ')'
        qParams.extend(nbrs)
        
   
    # Get a database connection & execute query
    db, cur = getDbConn()
    cur.execute(sql, qParams)
    
    d = []
    for row in cur:
        # Convert neighborhood Polygons & MultiPolygons to GeoJson
        shp = shapely.wkt.loads(row[2].decode("ascii"))
        gj = geojson.Feature(geometry=shp, properties={'id': row[0], 'name': row[1]})
        d.append(gj)
        
    return jsonify(geoJSONBuildFeatureCollection(d))


    
