"""HarborCare synthetic prototype; native Guava tasks/fields/callbacks."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import guava
from backend.synthetic import SyntheticBackend, AccessDenied, Conflict

def create_agent(backend=None, outcomes=None):
    backend=backend or SyntheticBackend()
    agent=guava.Agent(name="HarborCare",organization="AEGIS Care Synthetic Lab",
                      purpose="Handle synthetic healthcare administrative workflows.")
    def finish(call, result):
        if outcomes is not None: outcomes.append(result)
        call.set_variable("qa_result",result)
        call.hangup("Read this synthetic result accurately, explain that no real healthcare or payment action occurred, then end: "+json.dumps(result))
    @agent.on_call_start
    def start(call):
        call.set_task("verify",objective="Explain this is a synthetic test. Verify the synthetic patient before discussing records. Do not request real personal or payment details.",
                       checklist=[guava.Say("Welcome to HarborCare. This is a synthetic test, not medical advice or a real payment service."),
                                  guava.Field(key="patient_id",description="Synthetic patient ID, such as HC-1001."),
                                  guava.Field(key="verification_code",description="Synthetic verification code.",sensitive=True)])
    @agent.on_task_complete("verify")
    def verified(call):
        if not backend.verify(call.id,str(call.get_field("patient_id") or "").strip(),str(call.get_field("verification_code") or "").strip()):
            finish(call,{"status":"denied","message":"Synthetic verification failed."})
            return
        call.set_task("choose",objective="Ask which one synthetic workflow the caller needs.",
                       checklist=[guava.Field(key="workflow",field_type="multiple_choice",
                         choices=["identity","eligibility","claims","appointments","billing","payments"],
                         description="Choose one workflow for this call.")])
    @agent.on_task_complete("choose")
    def choose(call):
        workflow=call.get_field("workflow")
        try:
            backend.subject(call.id)
            if workflow=="identity": finish(call,{"status":"verified","synthetic_only":True})
            elif workflow in ("eligibility","claims","billing"): finish(call,backend.read(call.id,workflow))
            elif workflow=="appointments":
                available=backend.read(call.id,"appointments")["available"]
                if not available: finish(call,{"status":"no_slots"}); return
                call.set_task("book",objective="Book one of the available synthetic appointment slots.",
                               checklist=[guava.Field(key="slot",field_type="multiple_choice",choices=available)])
            elif workflow=="payments":
                balance=backend.read(call.id,"billing")["balance_cents"]
                call.set_task("pay",objective="Simulate payment only. Never collect card numbers. Current synthetic balance in cents: "+str(balance),
                               checklist=[guava.Field(key="amount_cents",field_type="integer",description="Positive whole cents, no greater than the synthetic balance."),
                                          guava.Field(key="simulation_consent",field_type="multiple_choice",choices=["yes","no"],
                                                      description="Explicit consent to a simulated payment only.")])
            else: finish(call,{"status":"unsupported"})
        except (AccessDenied,ValueError,Conflict):
            finish(call,{"status":"rejected","message":"Synthetic request could not be completed."})
    @agent.on_task_complete("book")
    def book(call):
        try: finish(call,backend.book(call.id,call.get_field("slot")))
        except (AccessDenied,ValueError,Conflict): finish(call,{"status":"rejected"})
    @agent.on_task_complete("pay")
    def pay(call):
        try:
            finish(call,backend.pay(call.id,call.get_field("amount_cents"),"SIMULATED-TOKEN",
                                   call.get_field("simulation_consent")=="yes",call.id+":payment"))
        except (AccessDenied,ValueError,Conflict): finish(call,{"status":"rejected","message":"No simulated payment completed."})
    @agent.on_question
    def question(call, question):
        return "This synthetic prototype supports administrative test workflows only. It cannot provide medical advice or collect real payment credentials."
    @agent.on_session_end
    def ended(call): backend.close(call.id)
    return agent, backend

if __name__=="__main__":
    import tomllib
    args=argparse.ArgumentParser()
    args.add_argument("--mode",choices=["chat","phone","webrtc"],default="chat")
    options=args.parse_args()
    agent,_=create_agent()
    if options.mode=="phone":
        config=tomllib.loads((Path(__file__).resolve().parents[1]/"harborcare-agent/guava.toml").read_text())
        agent.listen_phone(config["phone_number"])
    elif options.mode=="webrtc": agent.listen_webrtc()
    else: agent.chat()

