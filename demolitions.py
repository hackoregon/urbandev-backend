# Standard python imports
import os
import sys

# Web app imports
from flask import abort, request, Response, jsonify

# Our utilities & libs
import consts
from util import genMarkdownResult, getDbConn, geoJSONBuildFeatureCollection, wktUnpackPoint, geoJSONBuildPoint


def demolitions_api(fileext=None):
    
    if len(request.args) == 0:
        return genMarkdownResult('doc/demolitions.md')

    
    # Required argument. One of 'residential'. Will eventually support 'commercial' as well
    permitType = request.args.get('type')
    if not permitType:
        return make_response('Error: Must supply permitType arg', 400)
        
  
    # Read optional params
    bounds = request.args.get('bounds')    
    startDate = request.args.get('startdate')
    endDate = request.args.get('enddate')
    nbrhood = request.args.get('neighborhood')
    
    # Return JSON formatted table without spatial. 
    #if queryType and fileext == 'json':
    #    if queryType == 'perNeighborhoodPerYear':
    #        # Permits by neighborhood by year
    #        db, cur = getDbConn()
    #        #sql = "SELECT COUNT(*) AS num, year(issuedate) AS date_issued, nbrhood FROM permits2 " \
    #        #      "WHERE YEAR(issuedate) > 0 GROUP BY(YEAR(issuedate)), nbrhood"
    #
    #        # Filter out additions & alterations      
    #        sql = "SELECT COUNT(*) AS num, year(issuedate) AS date_issued, nbrhood FROM permits2 " \
    #              "WHERE YEAR(issuedate) > 0 AND new_class NOT IN ('ALTERATION', 'ADDITION') " \
    #              "GROUP BY(YEAR(issuedate)), nbrhood"
    #              
    #        cur.execute(sql)
    #        return jsonify({'query': 'perNeighborhoodPerYear',
    #                        'rows': [(row[0], row[1], row[2]) for row in cur]})
    #
    
        
        
    # Spatial Queries
    if fileext != 'geojson':
        return make_response('Error: Unknown file type extension', 400)
    
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
                     
    # Setup base SQL with spatial bounding box query
    sql = "SELECT AsText(shape), id, address, demolition_date, neighborhood " \
          "FROM demolitions WHERE MbrContains(PolygonFromText(%s), shape)"
    qParams = []
    

    # Optional start date & end date append to WHERE clause. ToDo: validate start & end date
    if startDate:
        sql += " AND demolition_date >= %%s"
        qParams = [startDate]
    
    if endDate:
        sql += " AND demolition_date <= %%s"
        qParams.append(endDate)

    # Comma delimited list of neighborhoods. Build SQL IN expression
    if nbrhood:
        nbrs = nbrhood.split(',')
        sql += " AND neighborhood IN (" + "%%s," * len(nbrs)
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
                    'demolition_date': row[3].isoformat() if row[3] else None,
                    'nbrhood': row[4]
                    }
                ))

    return jsonify(geoJSONBuildFeatureCollection(d))
        

