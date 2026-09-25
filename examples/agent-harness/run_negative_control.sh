#!/bin/sh
# Run a known mutant and require the focused suite to turn red.
# For a real project, replace demo_policy.py with a consequential contract.
set -eu
if [ "$#" -ne 1 ]; then
  echo "usage: run_negative_control.sh EXISTING_REPORT_DIRECTORY" >&2
  exit 2
fi
reports=$(cd "$1" && pwd -P)
here=$(cd "$(dirname "$0")" && pwd -P)
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
python -m pytest -q "$here/test_demo_policy.py" --junitxml="$reports/normal.xml"
set +e
AGENT_DELIBERATE_FAULT=1 python -m pytest -q "$here/test_demo_policy.py" --junitxml="$reports/deliberate-fault.xml"
fault_status=$?
set -e
if [ "$fault_status" -eq 0 ]; then
  echo "UNVERIFIED: the deliberate fault survived" >&2
  exit 1
fi
echo "Negative control passed: normal suite green, deliberate fault red"
