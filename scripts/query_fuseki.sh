#!/usr/bin/env sh
set -eu

QUERY_FILE="${1:-queries/open_claims.rq}"
SPARQL_URL="http://localhost:3030/policygraph/sparql"

if [ ! -f "$QUERY_FILE" ]; then
  echo "Missing query file: ${QUERY_FILE}" >&2
  exit 1
fi

curl -f -G -H "Accept: application/sparql-results+json" --data-urlencode "query@${QUERY_FILE}" "$SPARQL_URL"
