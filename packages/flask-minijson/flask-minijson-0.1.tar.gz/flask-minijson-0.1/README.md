flask-minijson
==============

[![Build Status](https://travis-ci.com/Dronehub/flask-minijson.svg)](https://travis-ci.com/Dronehub/flask-minijson)
[![Test Coverage](https://api.codeclimate.com/v1/badges/34b392b61482d98ad3f0/test_coverage)](https://codeclimate.com/github/Dronehub/flask-minijson/test_coverage)
[![Issue Count](https://codeclimate.com/github/Dronehub/flask-minijson/badges/issue_count.svg)](https://codeclimate.com/github/Dronehub/flask-minijson)
[![PyPI](https://img.shields.io/pypi/pyversions/flask-minijson.svg)](https://pypi.python.org/pypi/flask-minijson)
[![PyPI version](https://badge.fury.io/py/flask-minijson.svg)](https://badge.fury.io/py/flask-minijson)
[![PyPI](https://img.shields.io/pypi/implementation/flask-minijson.svg)](https://pypi.python.org/pypi/flask-minijson)

An extension for Flask to allow clients to submit data using the application/minijson codec

flask-json is required to be initialized before `FlaskMiniJSON`, in such a way:

```python
from flask_minijson import FlaskMiniJSON

app = Flask(__name__)
FlaskJSON(app)
FlaskMiniJSON(app)
```

And you use it like this:

```python
@app.route('/v1', methods=['POST'])
def endpoint():
    json = request.get_json()
```
if normal JSON is passed, it will be recognized. If
minijson is sent by the client, it will be recognized as well
