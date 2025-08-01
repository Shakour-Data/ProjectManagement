#!/usr/bin/env python3
import os
import sys
import datetime
import re
import json

TEST_DOCS_DIR = os.path.join(os.path.dirname(__file__), '../TestingDocs')
LOGS_DIR = os.path.join(os.path.dirname(__file__), '../TestLogs')

def update_test_document(test_type: str, test_results: dict):
    """
    Update the markdown test document for the given test_type with the latest test_results.
    test_results: dict with keys:
      - 'passed_tests': list of test ids or names that passed
      - 'failed_tests': list of test ids or names that failed
      - 'run_datetime': ISO format datetime string of test run
      - 'summary': short summary string of the test run
    """
    doc_filename = f"{test_type.replace(' ', '_')}.md"
    doc_path = os.path.join(TEST_DOCS_DIR, doc_filename)
    if not os.path.isfile(doc_path):
        print(f"Test document {doc_filename} not found in {TEST_DOCS_DIR}")
        return False

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prepare the test run summary entry
    run_dt = test_results.get('run_datetime', datetime.datetime.now().isoformat())
    summary = test_results.get('summary', '')
    passed = test_results.get('passed_tests', [])
    failed = test_results.get('failed_tests', [])

    summary_entry = f"\n\n---\n\n## Test Run Summary - {run_dt}\n\n"
    summary_entry += f"**Summary:** {summary}\n\n"
    summary_entry += f"**Passed Tests ({len(passed)}):**\n"
    for test in passed:
        summary_entry += f"- {test}\n"
    summary_entry += f"\n**Failed Tests ({len(failed)}):**\n"
    for test in failed:
        summary_entry += f"- {test}\n"

    # Append the summary entry at the end of the document
    if content.strip().endswith('---'):
        # Remove trailing separator to avoid duplicates
        content = content.rstrip('- \n')
    content += summary_entry + "\n---\n"

    # Update checklist items in the document
    def replace_checklist(match):
        checklist_text = match.group(0)
        for test in passed:
            # Mark passed tests as checked
            checklist_text = re.sub(rf"^- \[ \] {re.escape(test)}", f"- [x] {test}", checklist_text, flags=re.MULTILINE)
        for test in failed:
            # Mark failed tests as unchecked (or leave as is)
            checklist_text = re.sub(rf"^- \[x\] {re.escape(test)}", f"- [ ] {test}", checklist_text, flags=re.MULTILINE)
        return checklist_text

    # Regex to find checklist blocks (lines starting with - [ ] or - [x])
    content = re.sub(r"((?:^- \[[ x]\] .+\n?)+)", replace_checklist, content, flags=re.MULTILINE)

    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated test document: {doc_filename}")
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: update_test_docs.py <TestType> <TestResultsJSONFile>")
        print("Example: update_test_docs.py Unit_Testing test_results/unit_test_results.json")
        sys.exit(1)

    test_type = sys.argv[1].replace('_', ' ')
    results_file = sys.argv[2]

    if not os.path.isfile(results_file):
        print(f"Test results file not found: {results_file}")
        sys.exit(1)

    with open(results_file, 'r', encoding='utf-8') as f:
        test_results = json.load(f)

    success = update_test_document(test_type, test_results)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
