# Installation method test matrix
Updated: 2026-10-11. User confirmed "ifm" means PowerShell irm.

## Methods and attribution
| Method ID | Component/artifact | Method | Actual evidence/status |
| --- | --- | --- | --- |
| UV-SDK | Python guava-sdk package | uv venv then uv pip install guava-sdk==0.47.0 | Executed in isolated baseline; import/version verified; 8 offline runtime tests: 7 PASS, 1 FAIL |
| IRM-CLI | Windows guava.exe and install.ps1 | irm downloads script; iex executes script; script downloads binary | Current script inspected only, not executed; original installed CLI method UNKNOWN |
| DIRECT-CLI | Windows executable artifact | Direct local inspection, signature/hash/version checks | Existing CLI 0.47.0 verified; NotSigned; does not establish how it was installed |
| PIP-SDK | Python guava-sdk package | pip installation into separate environment | Optional comparison plan; NOT_RUN; not needed to infer uv behavior |
| CURL-CLI | Linux/macOS CLI installer | curl downloads installer; shell executes | Cross-platform plan only; NOT_RUN |

irm is a download command, not a Python package manager. The irm/iex route installs the CLI; uv installs the Python SDK here. They are not equivalent implementations of the same installer.
Classify an issue by component and reproduction, not solely installation method. SDK-F001 was reproduced in the uv environment but is SDK check_response behavior; no evidence makes it a uv-specific defect. CLI-F001 is a binary property independent of installation route. CLI-F002 belongs to the inspected current Windows installer.

## Method-specific cases
All additional cases below are NOT_RUN unless explicitly noted. Existing suite does not validate the package installer's integrity mechanisms.
| Case | Route | Setup and steps | Expected / evidence |
| --- | --- | --- | --- |
| UV-01 | UV-SDK | Create isolated environment; pin SDK; import; inventory dependencies | Exact version/import and inventory; already observed, only this runtime |
| UV-02 | UV-SDK | Preserve index metadata and artifact hash; build hash-locked dependency inputs; reject altered artifact in isolated test | Artifact mismatch rejected; authoritative provenance stated; NOT_RUN |
| UV-03 | UV-SDK | Test dependency resolution, unsupported Python and unavailable index in isolated environment | Actionable error and clear environment state; NOT_RUN |
| UV-04 | UV-SDK | Test cache/reinstall/offline reproducibility and read-only target in disposable environment | No unexpected privilege requirement; reproducible versions; failure state recorded; NOT_RUN |
| IRM-01 | IRM-CLI | Preserve exact script URL/date/hash; inspect version selection and download destination | Current source inspection completed; original historical installer unknown |
| IRM-02 | IRM-CLI | Inspect trusted-checksum comparison and signature/publisher enforcement | Both absent in inspected current script; runtime tamper/failure enforcement NOT_RUN |
| IRM-03 | IRM-CLI | Simulate interrupted download, denied destination and failed PATH update in isolation | Prior binary preserved; no partial activation; actionable error; NOT_RUN |
| IRM-04 | IRM-CLI | Simulate upgrade/reinstall/rollback against dummy prior artifact | Recoverable previous version; no unexpected overwrite or privilege escalation; NOT_RUN |
| BIN-01 | DIRECT-CLI | Inspect existing executable signature/hash and query version | Completed: 0.47.0, NotSigned; hashes in installer audit |
| CMP-01 | UV-SDK/PIP-SDK | Optional same SDK/runtime/resolved dependencies in separate environments; run identical contracts | Differences attributed to route only when artifacts/dependencies are controlled; NOT_RUN |

Authenticode checks Windows publisher signatures. Package-manager integrity tests concern package artifacts, indexes and trusted expected hashes; not every Python artifact is a Windows signed executable. Absence of installer verification does not prove absence of every package-manager control.

## Run record requirements
Include method ID, component, installation command (redacted), tool version, target SDK/CLI version, OS/Python, source URL/index, retrieved artifact hashes, dependency inventory, privilege/context, outcome, raw evidence and limitations.
For the installed existing CLI: installation_method=UNKNOWN, observation_method=DIRECT-CLI. Do not relabel it IRM-CLI merely because the current installer uses that route.
Runtime SDK contracts should include install route as environment metadata while keeping their pass/fail scoped to tested SDK behavior.
