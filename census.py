# Standard python imports
import os, sys

# Web app imports
from flask import request, Response

# Our utilities & libs
from util import genMarkdownResult


   
def census_api():
    return genMarkdownResult('doc/census.md')




