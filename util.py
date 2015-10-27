import flask

import tier


def getDbConn():
    '''Return a new database connection and cursor as a tuple of (connection, cursor)'''
    if not hasattr(flask.g, 'dbconn'):
        # Get factory & create new connection
        db = flask.current_app.config['DBCONN']
        flask.g.dbconn = db.connection, db.connection.cursor()
    return flask.g.dbconn
   
   
def wktUnpackPoint(wktstr):
    '''Unpack the point coordinates from WKT Point to a tuple'''
    p = wktstr.decode('ascii').split(' ') 
    i = p[1].rfind(')')
    return float(p[0][6:]), float(p[1][:i])
    
    
def geoJSONBuildFeatureCollection(wktFeatureList):
    body = {"type": "FeatureCollection","crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}},"features":None}
    body['features'] = [f for f in wktFeatureList]
    return body
    # If bbx supplied, insert it
    #"bbox": [ -123.48593, 44.88571, -121.67909, 45.93784 ],  
    
    
def geoJSONBuildPoint(lng, lat, prop_dict):
    return {'geometry': {'type': 'Point', 'coordinates': [lng, lat]}, 'type': 'Feature', 'properties': prop_dict}   


def genMarkdownResult(filename):
    '''Given a markdown file, return code to the browser to generate an HTML version 
    of that document using the strapdown.js library. Conversion is done in the client browser. 
    Useful for generating a documentation page for a service'''

    # Required strapdown.js markdown wrapper
    hdr = '''<!DOCTYPE html>
             <html>
             <head>
                 <title>{0}</title>
                 <script>{1}</script>
             </head>
             <xmp theme="united" style="display:none;">'''

    # Use CDN if developing
    if tier.APP_TIER == 'dev':
        kStrapPth = "http://strapdownjs.com/v/0.2/strapdown.js"
    else:
        kStrapPth = "/static/assets/strapdown/strapdown.js"
    
    ftr = '</xmp><script src="{0}"></script></html>'.format(kStrapPth)
    
    try:
        # Read Markdown file
        d = open(filename, 'r').readlines()
        jsext = open('doc/docapp.js', 'r').read()
    except IOError as e:
        return 'Exception: ' + str(e)
    else:
        if len(d) > 1:
            # Gen output - first line is title
            return hdr.format(d[0], jsext) + '\n'.join(d[1:]) + ftr
        else:
            return 'Error: Need more that one line in .md file'









def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
    

def site_map():
    '''Debug: Generate a list of urls and routes'''
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    # links is now a list of url, endpoint tuples
    print(links)
    return 'ok'  
    
    
    










