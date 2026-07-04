#!/usr/bin/env sh
set -eu

GRAPH_FILE="rdf/policygraph-combined.ttl"
DATASET_URL="http://localhost:3030/policygraph/data"
SPARQL_URL="http://localhost:3030/policygraph/sparql"

if [ ! -f "$GRAPH_FILE" ]; then
  echo "Missing rdf/policygraph-combined.ttl. Run python -m policygraph.materialize_graph first." >&2
  exit 1
fi

curl -f -X PUT -H "Content-Type: text/turtle" --data-binary "@${GRAPH_FILE}" "$DATASET_URL"
echo "SPARQL endpoint: ${SPARQL_URL}"
