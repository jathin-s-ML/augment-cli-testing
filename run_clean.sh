#!/bin/bash
# Clean wrapper to run any Python script without async warnings

# Suppress Python warnings
export PYTHONWARNINGS='ignore::RuntimeWarning'

# Run the script and redirect stderr to /dev/null to hide warnings
python "$@" 2>/dev/null

