#!/bin/bash

# Script to run all unit tests with coverage reporting

echo "Running all unit tests with coverage..."

# Run all unit tests with coverage, including all test files
python -m pytest Tests/TestingCode/UnitTests/test_main_modules/ \
    Tests/TestingCode/UnitTests/test_services/ \
    --cov=. \
    --cov-report=html:htmlcov_all \
    --cov-report=term-missing \
    --cov-config=.coveragerc \
    --verbose

echo "Coverage report generated in htmlcov_all directory"
echo "To view the report, run: python -m http.server 8000 --directory htmlcov_all"
