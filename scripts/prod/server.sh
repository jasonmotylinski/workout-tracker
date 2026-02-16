#!/usr/bin/env bash
cd /var/projects/workout-tracker
source venv/bin/activate
exec gunicorn --bind unix:/run/workout-tracker.sock run:app