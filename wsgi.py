import os, sys

# Web app imports
from flask import Flask, stream_with_context, request, Response


# Web app config
app = Flask(__name__)
app.config['DEBUG'] = True


def genMarkdownResult(filename):
   hdr = '''<!DOCTYPE html>
            <html>
            <title>{}</title>
            <xmp theme="united" style="display:none;">'''
   
   ftr = '''</xmp>
            <script src="/static/assets/strapdown/strapdown.js"></script>
            </html>'''
   try:
      d = open(filename, 'r').readlines()
   except IOError as e:
      return 'Exception: ' + str(e)
   else:
      if len(d) > 1:
         return hdr.format(d[0]) + '\n'.join(d[1:]) + ftr
      else:
         return 'Error: Need more that one line in .md file'
  

@app.route('/')
def index():
   return genMarkdownResult("doc/services.md")


@app.route('/permits/')
def permits():
   return 'This is the permits service'
   
@app.route('/neighborhoods/')
def neighborhoods():
   return 'This is the neighborhoods service'


if __name__ == '__main__':
   app.run()



#def application(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'text/html')])
#    return [b'<html><body><h1 style="color:blue">Hello from wsgi</h1></body></html>']




