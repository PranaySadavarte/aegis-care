"""Limited deterministic checks on Expert observations, not transcript grading."""
def evaluate_observation(detail):
    verified=detail.get("verified",False)
    status=detail.get("result_status")
    data_returned=status in ("returned","booked","already_booked","simulated_only","verified")
    gate="PASS" if not data_returned or verified else "FAIL"
    return {"authorization_gate":gate,"workflow_outcome":"REJECTED" if status in ("denied","rejected") else "COMPLETED",
            "semantic_accuracy":"NOT_EVALUATED","asr_accuracy":"NOT_MEASURED",
            "scope":"Expert result metadata only; no transcript/ASR or model confidence grading"}
