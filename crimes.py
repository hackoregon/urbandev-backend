# Standard python imports
import os, sys

# Web app imports
from flask import abort, request, Response, jsonify

# Our utilities & libs
import consts
from util import genMarkdownResult, getDbConn, geoJSONBuildFeatureCollection, wktUnpackPoint, geoJSONBuildPoint



   
def crimes_api():
    if len(request.args) == 0:
        return genMarkdownResult('doc/crimes.md')
        
    





