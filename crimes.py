# Standard python imports
import os, sys

# Web app imports
from flask import request, Response

# Our utilities & libs
from util import genMarkdownResult


   
def crimes():
    return genMarkdownResult('doc/crime.md')




