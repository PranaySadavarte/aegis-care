"""HarborCare synthetic prototype; native Guava tasks/fields/callbacks."""
import argparse
import json
import logging
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import guava
from backend.synthetic import SyntheticBackend, AccessDenied, Conflict

def create_agent(backend=None, outcomes=None, recorder=None):
    backend=backend or SyntheticBackend()
    from guava.helpers.llm import IntentRecognizer
    identity_intents=IntentRecognizer({"switch_patient":"Caller changes their identity or requests a different patient account; fresh verification is required."})
    agent=guava.Agent(name="HarborCare",organization="HarborCare",
                      purpose="Help callers with healthcare administration.")
    def finish(call, result):
        if recorder: recorder(call,"finished",{"workflow":call.get_field("workflow") or "verification","result_status":result.get("status","returned") if isinstance(result,dict) else "returned","verified":call.id in backend.authorized})
        if outcomes is not None: outcomes.append(result)
        call.set_variable("qa_result",result)
        if isinstance(result,dict) and result.get("status")=="denied":
            message="I could not verify those details. Please check your patient ID and code and call again."
        elif isinstance(result,dict) and "balance_cents" in result:
            message="Your account balance is "+format(result["balance_cents"]/100,".2f")+" dollars."
        elif isinstance(result,dict) and "plan" in result:
            message="Your plan is "+result["plan"]+". Coverage is "+("active." if result["active"] else "inactive.")
        elif isinstance(result,list):
            message="Your claim "+result[0]["id"]+" is "+result[0]["status"]+"." if result else "There are no claims on this account."
        elif isinstance(result,dict) and result.get("status") in ("booked","already_booked"):
            message="Your appointment is confirmed for "+result["slot"]+"."
        elif isinstance(result,dict) and result.get("status")=="simulated_only":
            message="Your demo payment of "+format(result["amount_cents"]/100,".2f")+" dollars is recorded. No real charge was made."
        elif isinstance(result,dict) and result.get("status")=="verified":
            message="Your identity check is complete."
        else: message="I am unable to complete this request right now. Please try again."
        call.hangup("Tell the caller this result naturally, then close courteously: "+message)
    @agent.on_call_start
    def start(call):
        if recorder: recorder(call,"started")
        call.set_task("verify",objective="Welcome the caller. Mention demo data once, briefly. Verify identity before discussing records. Never request real personal or card details.",
                       checklist=[guava.Say("Welcome to HarborCare. This demo uses sample records. I can help with your coverage, claims, appointments, or account."),
                                  guava.Field(key="patient_id",description="Collect synthetic patient ID as digits, such as 1001. Legacy HC-prefixed IDs also work."),
                                  guava.Field(key="verification_code",description="Collect the four-digit synthetic verification code as digits, preserving zeros. Do not guess or disclose a code. Legacy DEMO-prefixed codes also work.",sensitive=True)])
    @agent.on_task_complete("verify")
    def verified(call):
        if not backend.verify(call.id,str(call.get_field("patient_id") or "").strip(),str(call.get_field("verification_code") or "").strip()):
            logging.getLogger("harborcare").info("Synthetic verification denied; exact accepted credentials did not match. No credential values logged.")
            finish(call,{"status":"denied","message":"Synthetic verification failed."})
            return
        call.set_task("choose",objective="Ask how you can help with coverage, claims, appointments, billing or a demo payment. Use the matching workflow without naming internal test labels.",
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
    @agent.on_action_request
    def action_request(call,request):
        actions=identity_intents.classify(request)
        if actions and any(item.key=="switch_patient" for item in actions):
            backend.close(call.id)
            return [guava.SuggestedAction(key="switch_patient",description="Verify the different patient before any account access.")]
        return None
    @agent.on_action("switch_patient")
    def switch_patient(call):
        backend.close(call.id)
        call.set_task("switch_verify",objective="Explain that access to a different account requires fresh verification. Do not reuse the earlier code.",
                      checklist=[guava.Field(key="new_patient_id",description="The different patient ID."),
                                 guava.Field(key="new_verification_code",description="The code for that patient; never guess it.",sensitive=True)])
    @agent.on_task_complete("switch_verify")
    def switch_verified(call):
        if not backend.verify(call.id,str(call.get_field("new_patient_id") or ""),str(call.get_field("new_verification_code") or "")):
            finish(call,{"status":"denied"});return
        call.set_task("choose",objective="Ask how you can help with coverage, claims, appointments, billing or a demo payment.",
                      checklist=[guava.Field(key="workflow",field_type="multiple_choice",choices=["identity","eligibility","claims","appointments","billing","payments"])])
    @agent.on_question
    def question(call, question):
        return "I can help with coverage, claims, appointments and billing after verification. For medical questions, please contact your clinician. Please do not share card details."
    @agent.on_session_end
    def ended(call, event):
        if recorder: recorder(call,"ended",{"termination":event.termination_reason})
        backend.close(call.id)
    return agent, backend

def plain_text_chat(agent):
    """Simple terminal view built on native TestSession, not a new dialog engine."""
    from websockets.exceptions import ConnectionClosedOK
    with agent.test() as session:
        printed=0
        while True:
            try: session.wait_for_turn()
            except ConnectionClosedOK:
                print(session.get_transcript()[printed:]);break
            transcript=session.get_transcript();print(transcript[printed:]);printed=len(transcript)
            try:message=input("You: ").strip()
            except EOFError:break
            if message.lower() in ("quit","exit"):break
            if message:session.say(message)

if __name__=="__main__":
    import tomllib
    args=argparse.ArgumentParser()
    args.add_argument("--mode",choices=["chat","text","phone","webrtc","local"],default="chat")
    options=args.parse_args()
    from guava import logging_utils
    logging_utils.configure_logging()
    from backend.call_journal import CallJournal
    journal=CallJournal(Path(__file__).resolve().parents[1]/"evidence/2026-10-11/call-history/manual-events.jsonl",channel=options.mode)
    agent,_=create_agent(recorder=journal)
    if options.mode=="phone":
        config=tomllib.loads((Path(__file__).resolve().parents[1]/"harborcare-agent/guava.toml").read_text())
        agent.listen_phone(config["phone_number"])
    elif options.mode=="webrtc": agent.listen_webrtc()
    elif options.mode=="local": agent.call_local()
    elif options.mode=="text": plain_text_chat(agent)
    else: agent.chat()
