# SDK-X004: Empty RAG instance produces unscoped document query

## In plain language

An empty document collection sends no explicit key restriction. We need the vendor to explain how the server interprets this before calling it a data leak.

## Which test caught this?

**Case:** `SDK-X004`

**Detector:** `HelperAndTenacityCoverage.test_rag_empty_namespace_does_not_query_all_documents`

**Source:** `tests/sdk/test_extended_contracts.py`

**Relevant owner:** Guava SDK

**Execution layer:** Mocked retrieval boundary

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-x004)


**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** Empty RAG instance produces unscoped document query. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** Helpers / retrieval / authorization. **Owner category:** Guava SDK / installer.

**Problem:** Empty RAG instance produces unscoped document query

**Expected:** Empty namespace fails closed or passes an explicit empty key list.

**Actual:** No tracked keys led to document_keys=None at the query boundary. Populated namespace live tests were isolated. Empty live query was not sent.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/offline-corrected.txt`; SHA-256: `f77edf221a369c64c5ce55f1a62915dc975852115ef251d018e0cc3f24b163b9`.

```text
FAIL: test_rag_empty_namespace_does_not_query_all_documents (test_extended_contracts.HelperAndTenacityCoverage.test_rag_empty_namespace_does_not_query_all_documents)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\prana\aegis-care\tests\sdk\test_extended_contracts.py", line 108, in test_rag_empty_namespace_does_not_query_all_documents
    rag.ask('query');self.assertEqual(ask.call_args.kwargs['document_keys'],[])
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None != []

```

**Proposed owner action / workaround (not applied):** Reject empty-document asks; use unique populated namespaces. Ask Guava to confirm server interpretation of omitted keys.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
