# Competency Questions

PolicyGraph answers the tutorial competency questions through SPARQL query files,
SHACL shapes, service methods, and API routes.

| Question | Primary artifacts |
| --- | --- |
| CQ1. Given a customer, what policies belong to that customer? | `queries/account_context_construct.rq`, `PolicyGraphService.account_context_for_customer_c001`, `/accounts/C001/context.ttl` |
| CQ2. Given a policy, what coverages does it include? | `queries/account_context_construct.rq`, materialized `ex:hasCoverage` triples |
| CQ3. Given a policy, what claims have been filed against it? | `queries/account_context_construct.rq`, materialized `ex:claimAgainstPolicy` triples |
| CQ4. Which claims are open? | `queries/open_claims.rq`, `PolicyGraphService.open_claims`, `/claims/open` |
| CQ5. Which policies are active? | `queries/active_policies.rq`, `PolicyGraphService.active_policies`, `/policies/active` |
| CQ6. Which claims involve a coverage type that exists on the policy? | `queries/claims_with_unlisted_coverage_type.rq` identifies the inverse quality issue |
| CQ7. Which claims have loss dates outside the policy effective period? | `queries/claims_outside_policy_period.rq`, SHACL `ex:ClaimShape`, `/quality/claims-outside-policy-period` |
| CQ8. Which policies have missing or invalid policyholder references? | `queries/missing_policyholders.rq`, SHACL `ex:PolicyShape`, `/quality/missing-policyholders` |
| CQ9. Which coverages have limit and deductible values typed as decimals? | `ontology/policygraph.ttl`, `mappings/policygraph.rml.ttl`, `tests/test_materialized_graph.py` |
| CQ10. Which customer, policy, coverage, and claim facts should be returned together for a specific account context? | `queries/account_context_construct.rq`, `PolicyGraphService.account_context_for_customer_c001`, `/accounts/C001/context.ttl` |
