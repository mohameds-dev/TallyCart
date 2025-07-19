#!/bin/bash

echo "Running tests with coverage..."
coverage run --source='.' manage.py test

echo -e "\nCoverage Report:"
coverage report

echo -e "\nTo view detailed HTML report, run: coverage html" 