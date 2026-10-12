"""Live SDK smoke: synthetic only, no telephone calls or document uploads."""
import json
import time
import guava
agent = guava.Agent(name="AEGIS QA", organization="Synthetic Test",
                    purpose="Complete a synthetic SDK smoke test.")
collected = {}
@agent.on_call_start
def start(call):
    call.set_task("smoke", objective="Collect the caller's synthetic test code.",
                   checklist=[guava.Field(key="test_code", field_type="text",
                                           description="Ask for the synthetic test code.")])
@agent.on_task_complete("smoke")
def done(call):
    collected["test_code"] = call.get_field("test_code")
    call.hangup("Thank the caller and end the synthetic test.")
started = time.monotonic()
with agent.test() as session:
    session.wait_for_turn()
    session.say("My synthetic test code is AEGIS-TEST-42.")
    session.wait_for_end()
assert session.termination_reason == "bot-hangup", session.termination_reason
assert collected.get("test_code") == "AEGIS-TEST-42", collected
print(json.dumps({"mode": "hosted-text", "elapsed_seconds": time.monotonic()-started,
                  "termination_reason": session.termination_reason,
                  "transcript": session.get_transcript()}))

