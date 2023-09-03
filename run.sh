#!/bin/bash
source /home/ta/mysongnimelist/venv/bin/activate
cd /home/ta/mysongnimelist
waitress-serve --port 5001 --call "flask_app:create_app"