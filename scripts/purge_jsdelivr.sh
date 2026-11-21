#!/usr/bin/env bash
# Best-effort purge; the workflow marks failures as warnings, never failed publication.
set -euo pipefail

failed=0
for file in happ/MyRoute.json happ/happ-routing-link.txt; do
  url="https://purge.jsdelivr.net/gh/SpeedeMiner/MyRoute@main/${file}"
  echo "Purging ${file}"
  if ! body="$(curl --fail-with-body --silent --show-error --location \
      --retry 3 --retry-delay 2 --retry-all-errors \
      --connect-timeout 10 --max-time 30 "${url}")"; then
    echo "::warning::jsDelivr purge HTTP/network failure for ${file}"
    failed=1
    continue
  fi
  # An accepted request can return a JSON status; surface explicit errors if supplied.
  if ! BODY="$body" python3 -c '
import json, os, sys
try:
    result = json.loads(os.environ["BODY"])
except json.JSONDecodeError:
    sys.exit(0)  # HTTP success without a JSON body
if isinstance(result, dict) and (
    result.get("success") is False
    or result.get("status") in ("failed", "error")
):
    print(result, file=sys.stderr)
    sys.exit(1)
'; then
    echo "::warning::jsDelivr purge returned an error for ${file}"
    failed=1
  else
    echo "Purge request accepted: ${file}"
  fi
done
exit "$failed"
