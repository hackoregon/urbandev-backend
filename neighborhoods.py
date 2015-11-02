# Standard python imports
import os, sys
from collections import OrderedDict


# Web app imports
from flask import jsonify, request, Response

import geojson
import shapely.wkt

# Our utilities & libs
import consts
from util import genMarkdownResult, getDbConn, geoJSONBuildFeatureCollection


   
def neighborhoods_api(fileext=None):
    if len(request.args) == 0:
        return genMarkdownResult('doc/neighborhoods.md')   
   
    nbrhoods = request.args.get('name')
    bounds = request.args.get('bounds') 
    option = request.args.get('option')
    queryType = request.args.get('query')
    city = request.args.get('city', '')
    
    
    if fileext not in ('json', 'geojson'):
       return make_response('Error: missing or invalid file extension', 400)
    
    
    if queryType and fileext == 'json':
        
        if queryType == 'list':
            # Return just neighborhood list. Filter by city
            sql = "SELECT distinct(name) FROM neighborhoods ORDER BY name" 
            
            # If city is Portland, just use the view 'portland_neighborhoods'
            if city == 'portland':
                sql = "SELECT name FROM portland_neighborhoods ORDER BY name"
            
            db, cur = getDbConn()
            cur.execute(sql)
            return jsonify({'query': 'list',
                            'rows': [row[0] for row in cur]})
            
        elif queryType == 'listWithBBX':
            # Return neighborhood list w/ BBX of each shape. Filter by city
            sql = "SELECT name, astext(St_envelope(shape)), area FROM urbandev_stg.neighborhoods "
            if city == 'portland':
                sql += "WHERE in_portland='t'"            
            sql += " ORDER BY name"
            
            db, cur = getDbConn()
            cur.execute(sql)
            
            result = []
            nbrs = OrderedDict()
            
            for row in cur:
                # Change WKT Polygon to Rect 
                ply = row[1].decode("utf8")
                rectP1 = ply[9:-2].split(',')
                
                p1 = rectP1[0].split(' ')
                p2 = rectP1[2].split(' ')
                
                # Array of 2 arrays [y1, x1], [y2, x2]
                #rectP2 = ((float(p1[1]), float(p1[0])), (float(p2[1]), float(p2[0])))
                rectP2 = ((float(p1[0]), float(p1[1])), (float(p2[0]), float(p2[1])))
                
                # There are multiple records for multi-part neighborhood polygons & we 
                # want a unique list so for now, we just pick the polygon with the 
                # greatest area.
                
                # ToDo: fix by calculating the combined BBX of all the polygons instead
                
                # Add name & rect if not already in dict. (May be able to use setdefault()?)
                if row[0] not in nbrs:
                    nbrs[row[0]] = (row[2], rectP2)
                else:
                    # If already in dict, update record if new area is greater 
                    if nbrs[row[0]][0] < row[2]:
                        nbrs[row[0]] = (row[2], rectP2)

            return jsonify({
                'query': 'listWithBBX', 
                'rows': [(k, v[1]) for k, v in nbrs.items()]
            })
    
    

    if fileext == 'geojson':
        # Return neighborhood polygons as GeoJSON features
        if bounds:
            try:
                # bounds is x1, y1, x2, y2
                ext = [float(pt) for pt in bounds.split(',')]
            except ValueError:
                return make_response('Error: Bounds values must be floats', 400)
        else:
            # Use the default BBX of the entire city
            ext = consts.PDX_BOUNDING_BOX

        # POLYGON(x1 y1, x1 y2, x2 y2, x2 y1, x1 y1)
        mbrPolyWKT = "'POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))'" % (ext[0], ext[1], ext[0], \
                     ext[3], ext[2], ext[3], ext[2], ext[1], ext[0], ext[1])
                     
        # Base sql
        sql = "SELECT id, name, AsText(shape) FROM neighborhoods "
        
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
            # Convert neighborhood Polygons & MultiPolygons to GeoJson. If this profiles to be slow
            # are a great opportunities for caching the GeoJSON 
            shp = shapely.wkt.loads(row[2].decode("ascii"))
            gj = geojson.Feature(geometry=shp, properties={'id': row[0], 'name': row[1]})
            d.append(gj)
            
        return jsonify(geoJSONBuildFeatureCollection(d))


    
