# Standard python imports
import os
import sys

# Web app imports
from flask import abort, request, Response, jsonify

# Our utilities & libs
import consts
from util import genMarkdownResult, getDbConn, geoJSONBuildFeatureCollection, wktUnpackPoint, geoJSONBuildPoint


def permits_api(ext=None):
    
    if len(request.args) == 0:
        return genMarkdownResult('doc/permits.md')
    
    # Required argument. One of 'residential' or 'query'. Will eventually support 'commercial' as well
    option = request.args.get('option')
    if not option:
        return 'Error: Must supply option arg'
        
    # Read optional params
    bounds = request.args.get('bounds')    
    startDate = request.args.get('startdate')
    endDate = request.args.get('enddate')
    nbrhood = request.args.get('neighborhood')
    
    # Permits by neighborhood by year
    if option == 'query':
        queryType = request.args.get('query')
            
        if queryType == 'permitsPerNeighborhoodPerYear':
            db, cur = getDbConn()
            sql = "SELECT COUNT(*) AS num, year(issuedate) AS date_issued, nbrhood FROM urbandev_stg.permits2 " \
                  "WHERE YEAR(issuedate) > 0 GROUP BY(YEAR(issuedate)), nbrhood"
            cur.execute(sql)
            return jsonify({'query': 'permitsPerNeighborhoodPerYear',
                            'rows': [(row[0], row[1], row[2]) for row in cur]})
        
        
    # Spatial Queries
    
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
                     
    # Setup base SQL with spatial bounding box query
    sql = "SELECT AsText(shape), id, address, issuedate, nbrhood FROM permits2 WHERE MbrContains(PolygonFromText(%s), shape)"
    qParams = []
    
    # Optional start date & end date append to WHERE clause. ToDo: validate start & end date
    if startDate:
        sql += " AND issuedate >= %%s"
        qParams = [startDate]
    
    if endDate:
        sql += " AND issuedate <= %%s"
        qParams.append(endDate)
    
    # Comma delimited list of neighborhoods. Build SQL IN expression
    if nbrhood:
        nbrs = nbrhood.split(',')
        sql += " AND nbrhood IN (" + "%%s," * len(nbrs)
        sql = sql[:-1] + ')'
        qParams.extend(nbrs)


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
        

