#!/bin/bash
echo "Starting Gunicorn server..."
gunicorn -b 0.0.0.0:$PORT app:app
