#!/bin/zsh
# Activate the virtual environment and run the Python script

source ~/venvs/ailib/bin/activate
exec python /configuration/scripts/indoor_soil_moisture_info.py
