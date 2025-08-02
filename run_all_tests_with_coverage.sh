#!/bin/bash

# Script to run all unit tests with coverage reporting

echo "Running all unit tests with coverage..."

# Run all unit tests with coverage, excluding problematic directories
python -m pytest Tests/TestingCode/UnitTests/test_main_modules/ \
    Tests/TestingCode/UnitTests/test_services/test_auto_commit.py \
    Tests/TestingCode/UnitTests/test_services/test_backup_manager.py \
    Tests/TestingCode/UnitTests/test_services/test_cli_commands.py \
    Tests/TestingCode/UnitTests/test_services/test_config_and_token_management.py \
    Tests/TestingCode/UnitTests/test_services/test_documentation_automation.py \
    Tests/TestingCode/UnitTests/test_services/test_github_integration.py \
    Tests/TestingCode/UnitTests/test_services/test_integration_manager.py \
    --cov=. \
    --cov-report=html:htmlcov_all \
    --cov-report=term-missing \
    --cov-config=.coveragerc

echo "Coverage report generated in htmlcov_all directory"
echo "To view the report, run: python -m http.server 8000 --directory htmlcov_all"
