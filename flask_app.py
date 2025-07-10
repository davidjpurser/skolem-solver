
from flask import Flask, request, jsonify, make_response, send_from_directory, abort
import os
import skolemtool
import time
import sys
import locale
import json


app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)
HTML_DIR = os.path.join(BASE_DIR, 'html')
ALLOWED_ALGORITHMS = {'bakerdavenport', 'leapfrogging'}

# 1. /skolem route
@app.route('/skolem', methods=['POST'])
def skolem_handler():
    # Debug info (you can remove these in production)
    print(time.time())
    print(sys.version_info)
    print(sys.stdout.encoding)
    print(locale.getpreferredencoding())

    # Parse JSON body
    try:
        data = request.get_json(force=True) or {}
    except Exception as e:
        return json.dumps({'status': 'fail', 'error': str(e)}), 400

    print(data)

    # Run the Skolem tool
    try:
        output = skolemtool.computeFromString(data['val'], data['options'])
    except Exception as e:
        return json.dumps({'status': 'fail', 'error': str(e)}), 400

    # Convert to JSON
    def convert(o):
        return str(o)

    json_output = json.dumps(output, default=convert)

    status_code = 400 if output.get('status') == 'fail' else 200
    response = make_response(json_output, status_code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


# 2. /algorithm/<x>/<y> route
@app.route('/algorithm/<x>/<path:y>')
def algorithm_handler(x, y):
    if x not in ALLOWED_ALGORITHMS:
        abort(404)
    # File is located at BASE_DIR/algorithm/x/html/y
    file_dir = os.path.join(BASE_DIR, x, 'html')
    return send_from_directory(file_dir, y)


# 3. Fallback route: serve from html/ directory
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(HTML_DIR, filename)

# 4. Optional: root route (like serving index.html)
@app.route('/')
def index():
    return send_from_directory(HTML_DIR, 'index.html')

