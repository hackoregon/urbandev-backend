# Standard python imports
import os, sys

# Web app imports
from flask import abort, request, Response, jsonify, make_response

# Our utilities & libs
import consts
from util import genMarkdownResult, getDbConn



   
def crimes_api(fileext=None):
    if len(request.args) == 0:
        return genMarkdownResult('doc/crimes.md')
        
    queryType = request.args.get('query')
    year = request.args.get('year')
    crimeCls = request.args.get('class', '')
    
    # Remove later if we return spatial data
    if fileext != 'json':
        return make_response('Error: Must use file extension .json (for now)', 400)
    
    
    if queryType and fileext == 'json':
        if queryType == 'perNeighborhoodPerYear':
            if not year:
                return make_response('Error: must supply year parameter', 400)
                
            startRange = year + '-01-01'
            try:
                endRange = int(year)
            except ValueError:
                return make_response('Error: year must be a number between 2004->2014', 400)
            
            endRange = str(endRange+1) + '-01-01'
            
            sql = "SELECT a.neighborhood as name, count(*) as count FROM crime3 a JOIN portland_neighborhoods b ON a.neighborhood=b.name " \
                  "WHERE a.report_datetime >= %s and a.report_datetime < %s GROUP BY a.neighborhood"

            if crimeCls == 'violent':
                sql = sql.replace('GROUP BY', "AND a.violent='t' GROUP BY") 
            elif crimeCls == 'nonviolent':
                sql = sql.replace('GROUP BY', "AND a.violent='f' GROUP BY") 
            else:
                # Just for returning to the caller
                crimeCls = 'all'
                
            db, cur = getDbConn()
            cur.execute(sql, (startRange, endRange))
            return jsonify({'query': 'perNeighborhoodPerYear', 'class': crimeCls, 'year': year,
                            'rows': [(row[0], row[1]) for row in cur]})


    return make_response('Error: unknown query option', 400)



