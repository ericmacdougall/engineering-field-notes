#!/bin/sh
# Illustrative command-hook wrapper for fixture policy JSON on stdin.
# A real host's event schema, matcher, exit semantics and delegation paths must
# be checked on the installed version. This sample is not a production policy.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$here/policy.py"
