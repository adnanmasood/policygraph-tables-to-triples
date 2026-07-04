# Modeling Notes

Tables are storage structures, not the semantic model. PolicyGraph uses the CSVs
as source data and then promotes durable business entities into RDF resources:
customers, policies, coverages, and claims.

Foreign keys become object properties. For example, `policies.customer_id`
becomes `ex:hasPolicyholder`, and `claims.policy_id` becomes
`ex:claimAgainstPolicy`.

Important codes become controlled resources. Policy status, claim status, and
coverage type values are represented as code IRIs and described in SKOS concept
schemes rather than modeled only as raw strings.

OWL/RDFS defines vocabulary and intended meaning. SHACL defines closed-world data
quality constraints. SPARQL answers application and quality questions. Keeping
those responsibilities separate makes the tutorial easier to test and reason
about.

RDF and OWL use open-world assumptions: absence of a triple does not prove a fact
is false. SHACL validation intentionally uses a closed-world view of the explicit
data graph so missing policyholders and invalid coverage references are detected.

The readable example IRIs are suitable for a tutorial. Production systems should
avoid PII in IRIs, use durable opaque identifiers where appropriate, and govern
namespace/version changes.
