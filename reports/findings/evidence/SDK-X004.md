# SDK-X004: Empty RAG instance produces unscoped document query

## In plain language

An empty document-search helper sends no document restriction. It sends None instead of an explicit empty list. Wider search or wrong-source answers are possible only if the server interprets missing restrictions that way; no leak was demonstrated.

## Which test caught this?

**Case:** `SDK-X004`

**Detector:** `HelperAndTenacityCoverage.test_rag_empty_namespace_does_not_query_all_documents`

**Source:** `tests/sdk/test_extended_contracts.py`

**Relevant owner:** Guava SDK

**Execution layer:** Mocked retrieval boundary

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-x004)


## Expected input and what could happen

RAG means looking up relevant documents before answering. Think of a helper as a search folder, and document keys as the names of the files it is allowed to search. This probe concerns native ServerRAG; HarborCare's six live workflows read our synthetic backend, not this document helper.

**Actual tested input:** an empty ServerRAG instance with namespace `audit-empty`, no tracked document keys, and the question `query`. Its retrieval call was replaced with a mock so no document search reached the server.

```text
Known documents in this instance: none
Expected safety outcome: refuse the search or explicitly restrict it to no documents
Actual client argument: document_keys = None
Our assertion expected: document_keys = []
Result: AssertionError: None != []
```

`[]` means an explicitly empty list. `None` means no list was supplied. They are different values. Whether the server treats either value as unrestricted must be confirmed with Guava; an empty list is not itself a proven server-side protection.

**Possible consequence:** if missing keys mean search everything the account can access, an empty collection could answer from unrelated documents instead of saying it has nothing to search. That could produce incorrect answers or expose documents outside the application's intended selection. It does not demonstrate access beyond the account's permissions or across organizations.

**Confirmed:** the omitted restriction at the client boundary. **Not confirmed:** a broader live search, confidential document return or data leak. The populated-document control passed a specific allowed key; the empty live query was deliberately not sent.

**Safe proposed workaround:** reject empty collections before asking, require a nonempty allowlist of intended keys, and confirm server semantics. Do not assume merely adding a namespace label enforces permission. No application or SDK fix was applied.


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
