#! /usr/bin/env python

import tempfile
import os
from executor import execute
from flask import Flask, request, make_response, abort

app = Flask(__name__)

@app.route('/', methods=['POST'])
def htmltopdf():

    args = ['wkhtmltopdf']

    source_file = tempfile.NamedTemporaryFile(suffix='.html')
    header_file = tempfile.NamedTemporaryFile(suffix='.html')
    footer_file = tempfile.NamedTemporaryFile(suffix='.html')
    cover_file = tempfile.NamedTemporaryFile(suffix='.html')
    

    if 'header' in request.files:
        header_file.write(request.files['header'].read())
        header_file.flush()
        args += ["--header-html", header_file.name]

    if 'footer' in request.files:
        footer_file.write(request.files['footer'].read())
        footer_file.flush()
        args += ["--footer-html", footer_file.name]

    if 'cover' in request.files:
        cover_file.write(request.files['cover'].read())
        cover_file.flush()
        args += ["cover", cover_file.name]

    if 'file' in request.files:
        source_file.write(request.files['file'].read())
        source_file.flush()
        args += [source_file.name, source_file.name + ".pdf"]
    else:
        app.logger.warning('no file in request.files: %s', request.files)
        abort(400)

    # Execute the command using executor
    execute(' '.join(args))

    with open(source_file.name + '.pdf', 'r') as myfile:
        data = myfile.read()
    os.unlink(source_file.name + ".pdf")

    resp = make_response(data)
    resp.headers['mimetype'] = 'application/pdf'
    
    return resp

@app.route('/liveness')
def liveness():
    return "OK"
