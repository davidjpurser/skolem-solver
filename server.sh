#!/bin/bash

# Run Flask app using gunicorn via Sage
sage --python -m gunicorn -w 4 flask_app:app
