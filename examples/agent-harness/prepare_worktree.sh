#!/bin/sh
# Create one isolated checkout. Never reuse a run directory.
set -eu
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "usage: prepare_worktree.sh REPO EXISTING_RUN_PARENT RUN_ID [REF]" >&2
  exit 2
fi
repo=$(cd "$1" && pwd -P)
parent=$(cd "$2" && pwd -P)
run_id=$3
if [ "$#" -eq 4 ]; then ref=$4; else ref=HEAD; fi
case "$run_id" in
  ""|*[!a-zA-Z0-9_-]*) echo "Invalid RUN_ID" >&2; exit 2 ;;
esac
actual_root=$(git -C "$repo" rev-parse --show-toplevel)
actual_root=$(cd "$actual_root" && pwd -P)
if [ "$actual_root" != "$repo" ]; then
  echo "REPO must be the exact Git root" >&2
  exit 2
fi
target=$parent/$run_id
if [ -e "$target" ]; then
  echo "Refusing to reuse an existing run directory" >&2
  exit 2
fi
git -C "$repo" worktree add --detach "$target" "$ref"
printf '%s\n' "$target"
