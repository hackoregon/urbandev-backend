# Standard python imports
import os
import sys

# Web app imports
from flask import abort, request, Response, jsonify

# Our utilities & libs
from util import genMarkdownResult, getDbConn, geoJSONBuildFeatureCollection, wktUnpackPoint, geoJSONBuildPoint


def permits():
    
    # Required argument. Will eventually support 'commercial' as well
    permitType = request.args.get('type')
    if not permitType:
        return genMarkdownResult('doc/permits.md')
        
    # Read optional params
    bounds = request.args.get('bounds')    
    startDate = request.args.get('startdate')
    endDate = request.args.get('enddate')
    
    if bounds:
        # bounds is x1, y1, x2, y2
        try:
            ext = [float(pt) for pt in bounds.split(',')]
        except ValueError:
            return 'Error: Bounds values must be floats'
    else:
        # Use the default BBX of the entire city
        #ext = (-123.0, 44.0, -122.0, 45.0)
        ext = (-122.9, 45.35, -122.4, 45.7)
        
    # POLYGON(x1 y1, x1 y2, x2 y2, x2 y1, x1 y1)
    mbrPolyWKT = "'POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))'" % (ext[0], ext[1], ext[0], \
                 ext[3], ext[2], ext[3], ext[2], ext[1], ext[0], ext[1])
                     
    # Setup base SQL with spatial bounding box query
    sql = "SELECT AsText(shape), id, address, issuedate, nbrhood FROM permits2 WHERE MbrContains(PolygonFromText(%s), shape)"
    qParams = []
    
    # Optional start date & end date append to WHERE clause
    if startDate:
        sql += " AND issuedate >= %%s"
        qParams = [startDate]
    if endDate:
        sql += " AND issuedate <= %%s"
        qParams.append(endDate)
    
    # Get a database connection & execute query
    db, cur = getDbConn()
    cur.execute(sql % (mbrPolyWKT,), qParams)
   
    # Convert result to GeoJSON using default CRS
    d = []
    for row in cur:
        d.append(geoJSONBuildPoint(*wktUnpackPoint(row[0]), prop_dict={
                    'id': row[1], 
                    'address': row[2],           
                    'issuedate': row[3].isoformat() if row[3] else None,
                    'nbrhood': row[4]
                    }
                ))

    return jsonify(geoJSONBuildFeatureCollection(d))
        

