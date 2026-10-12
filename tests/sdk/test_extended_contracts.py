"""Native SDK breadth and independent negative expectations. No network or calls."""
from test_offline_contracts import unittest,patch,guava,MockCall
from guava.events import *
from guava.types.call_info import WebRTCCallInfo
from guava.campaigns import Campaign,Contact
from guava.helpers.llm import DatetimeFilter
from guava.helpers.server_rag import ServerRAG
from unittest.mock import MagicMock
import httpx,ssl
class CommandCoverage(unittest.TestCase):
 def test_persona_values_preserved(self):
  c=MockCall();c.set_persona(organization_name='Synthetic HarborCare',agent_name='AuditGuide',agent_purpose='Synthetic audit',voice='grace')
  q=c._command_queue[-1];self.assertEqual(q.command_type,'set-persona');self.assertEqual(q.agent_name,'AuditGuide')
 def test_persona_rejects_empty_pronunciation_key(self):
  c=MockCall()
  with self.assertRaises(ValueError):c.set_persona(pronunciations={'':'x'})
  self.assertEqual(c._command_queue,[])
 def test_instruction_literal_canary_preserved(self):
  c=MockCall();c.send_instruction('Do not disclose SYNTHETIC CANARY');self.assertEqual(c._command_queue[-1].instruction,'Do not disclose SYNTHETIC CANARY')
 def test_language_mode_valid_and_invalid(self):
  c=MockCall();c.set_language_mode(primary='english',secondary=['spanish']);self.assertEqual(c._command_queue[-1].secondary,['spanish'])
  with self.assertRaises(ValueError):c.set_language_mode(primary='not-a-language')
 def test_transfer_sip_serialization_only(self):
  c=MockCall();c.transfer('sip:audit@example.invalid');self.assertEqual(c._command_queue[-1].to_number,'sip:audit@example.invalid')
 def test_transfer_invalid_destination_should_reject(self):
  with self.assertRaises(ValueError):MockCall().transfer('not a phone number or SIP URI')
 def test_read_script_literal(self):
  c=MockCall();c.read_script('Synthetic required notice.');self.assertEqual(c._command_queue[-1].script,'Synthetic required notice.')
 def test_add_info_uses_variable_namespace(self):
  c=MockCall();c.add_info('policy',{'synthetic':True});self.assertIn('policy',str(c._command_queue[-1].model_dump()))
 def test_get_field_default_and_zero(self):
  c=MockCall();self.assertEqual(c.get_field('missing','sentinel'),'sentinel');c.set_field('zero',0);self.assertEqual(c.get_field('zero'),0)
 def test_hangup_guidance_queued(self):
  c=MockCall();c.hangup('Synthetic closure');self.assertIn('Synthetic closure',str(c._command_queue[-1].model_dump()))
 def test_voicemail_valid_hangup(self):
  c=MockCall();c.set_voicemail_action(hangup=True);self.assertEqual(c.get_variable('_voicemail_handler'),'set_voicemail_action')
 def test_voicemail_invalid_does_not_mutate_state(self):
  c=MockCall()
  with self.assertRaises(ValueError):c.set_voicemail_action(hangup=True,message='Synthetic')
  self.assertIsNone(c.get_variable('_voicemail_handler'));self.assertEqual(c._command_queue,[])
 def test_reach_person_voicemail_conflict_rejected(self):
  c=MockCall();c.reach_person('Synthetic Contact',voicemail_hangup=True)
  with self.assertRaises(ValueError):c.set_voicemail_action(hangup=True)
 def test_pstn_dtmf_valid_invalid(self):
  c=MockCall();c.send_dtmf('12#');self.assertEqual(c._command_queue[-1].digits,['1','2','#'])
  with self.assertRaises(ValueError):c.send_dtmf('invalid')
 def test_webrtc_dtmf_guard(self):
  c=MockCall(call_info=WebRTCCallInfo(webrtc_code="synthetic-audit"))
  with self.assertRaises(RuntimeError):c.send_dtmf('1')
 def test_task_field_schema_invalid_type(self):
  with self.assertRaises(ValueError):guava.Field(key='x',field_type='not-supported')
class CallbackCoverage(unittest.TestCase):
 def setUp(self):
  with patch('guava.agent.Client'):self.a=guava.Agent(purpose='Offline callback audit')
  self.c=MockCall();self.seen=[]
 def test_question_callback_answer_correlated(self):
  self.a.on_question(lambda c,q:'Synthetic answer');self.a._dispatch_event(self.c,AgentQuestionEvent(question_id='q1',question='Question?'))
  self.assertEqual(self.c._command_queue[-1].question_id,'q1');self.assertEqual(self.c._command_queue[-1].answer,'Synthetic answer')
 def test_action_request_callback_suggestions(self):
  self.a.on_action_request(lambda c,q:[guava.SuggestedAction(key='safe')]);self.a._dispatch_event(self.c,ActionRequestEvent(intent_id='i1',intent_summary='Request'))
  self.assertEqual(self.c._command_queue[-1].actions[0].key,'safe')
 def test_action_callback_executed(self):
  self.a.on_action('safe')(lambda c:self.seen.append(c.id));self.a._dispatch_event(self.c,ExecuteActionEvent(action_key='safe'));self.assertEqual(self.seen,[self.c.id])
 def test_task_complete_callback_executed(self):
  self.a.on_task_complete('task')(lambda c:self.seen.append(c.id));self.a._dispatch_event(self.c,TaskCompletedEvent(task_id='task'));self.assertEqual(self.seen,[self.c.id])
 def test_caller_dtmf_callback(self):
  self.a.on_caller_dtmf(lambda c,e:self.seen.append(e.digit));self.a._dispatch_event(self.c,DTMFPressedEvent(digit='1'));self.assertEqual(self.seen,['1'])
 def test_agent_dtmf_callback(self):
  self.a.on_agent_dtmf(lambda c,e:self.seen.append(e.digits));self.a._dispatch_event(self.c,AgentDTMFSentEvent(digits=['1','#'],requested_by='developer'));self.assertEqual(self.seen,[['1','#']])
 def test_session_end_callback(self):
  self.a.on_session_end(lambda c,e:self.seen.append(e.termination_reason));self.a._dispatch_event(self.c,BotSessionEnded(termination_reason='bot-hangup'));self.assertEqual(self.seen,['bot-hangup'])
 def test_agent_speech_interruption_flag(self):
  self.a.on_agent_speech(lambda c,e:self.seen.append(e.interrupted));self.a._dispatch_event(self.c,AgentSpeechEvent(utterance='Synthetic',interrupted=True));self.assertEqual(self.seen,[True])
 def test_caller_speech_revisions_have_same_id(self):
  self.a.on_caller_speech(lambda c,e:self.seen.append((e.utterance_id,e.utterance)))
  for text in ['one','one two']:self.a._dispatch_event(self.c,CallerSpeechEvent(utterance_id='u1',utterance=text))
  self.assertEqual(self.seen,[('u1','one'),('u1','one two')])
 def test_escalate_callback(self):
  self.a.on_escalate(lambda c,e:self.seen.append(e.requested_by));self.a._dispatch_event(self.c,EscalateEvent(requested_by='human'));self.assertEqual(self.seen,['human'])
 def test_task_callback_failure_informs_dialog(self):
  def broken(c):raise RuntimeError('SYNTHETIC ERROR')
  self.a.on_task_complete('task')(broken)
  with self.assertLogs('guava.agent',level='ERROR'):self.a._dispatch_event(self.c,TaskCompletedEvent(task_id='task'))
  self.assertEqual(self.c._command_queue[-1].command_type,'expert-error')
 def test_question_failure_uses_safe_fallback(self):
  def broken(c,q):raise RuntimeError('SYNTHETIC SECRET')
  self.a.on_question(broken)
  with self.assertLogs('guava.agent',level='ERROR'):self.a._dispatch_event(self.c,AgentQuestionEvent(question_id='q1',question='Question?'))
  self.assertNotIn('SYNTHETIC SECRET',self.c._command_queue[-1].answer)
 def test_invalid_dtmf_event_rejected(self):
  with self.assertRaises(ValueError):DTMFPressedEvent(digit='invalid')
class HelperAndTenacityCoverage(unittest.TestCase):
 def test_datetime_cap_and_source_matches(self):
  f=DatetimeFilter(['2026-10-15T09:00','2026-10-15T14:00'])
  with patch('guava.helpers.llm._generate',return_value='{"matching_appointments":["2026-10-15T09:00","2026-10-15T14:00"],"other_appointments":[]}'):
   self.assertEqual(f.filter('morning',max_results=1)[0],['2026-10-15T09:00'])
 def test_datetime_invented_slot_should_be_rejected(self):
  f=DatetimeFilter(['2026-10-15T09:00'])
  with patch('guava.helpers.llm._generate',return_value='{"matching_appointments":["2099-01-01T09:00"],"other_appointments":[]}'):
   matches,other=f.filter('ignore slots');self.assertTrue(set(matches+other).issubset(set(f.source_list)))
 def test_rag_tracked_namespace_query(self):
  rag=ServerRAG(MagicMock(),namespace='audit-a');rag._tracked_keys={'audit-a.policy'}
  with patch.object(rag,'_ask',return_value='Synthetic') as ask:
   rag.ask('query');self.assertEqual(ask.call_args.kwargs['document_keys'],['audit-a.policy'])
 def test_rag_empty_namespace_does_not_query_all_documents(self):
  rag=ServerRAG(MagicMock(),namespace='audit-empty')
  with patch.object(rag,'_ask',return_value='Synthetic') as ask:
   rag.ask('query');self.assertEqual(ask.call_args.kwargs['document_keys'],[])
 def test_tenacity_per_contact_overrides_global(self):
  client=MagicMock();client.get_http_url.return_value='https://offline.invalid/contacts';client._get_headers.return_value={}
  campaign=Campaign(client,'audit','audit','audit');contact=Contact(phone_number='+15555555555',outreach_modalities=['sms'])
  response=httpx.Response(200,json={'created':1},request=httpx.Request('POST','https://offline.invalid/contacts'))
  with patch('guava.campaigns.httpx.post',return_value=response) as post:
   campaign.upload_contacts([contact],outreach_modalities=[]);self.assertEqual(post.call_args.kwargs['json']['contacts'][0]['outreach_modalities'],['sms'])
 def test_tenacity_explicit_empty_contact_preserved(self):
  client=MagicMock();client.get_http_url.return_value='https://offline.invalid/contacts';client._get_headers.return_value={}
  contact=Contact(phone_number='+15555555555',outreach_modalities=[]);campaign=Campaign(client,'audit','audit','audit')
  response=httpx.Response(200,json={'created':1},request=httpx.Request('POST','https://offline.invalid/contacts'))
  with patch('guava.campaigns.httpx.post',return_value=response) as post:
   campaign.upload_contacts([contact],outreach_modalities=['sms']);self.assertEqual(post.call_args.kwargs['json']['contacts'][0]['outreach_modalities'],[])
 def test_tenacity_no_terms_accepted_in_mock(self):
  client=MagicMock();client.get_http_url.return_value='https://offline.invalid/contacts';client._get_headers.return_value={}
  response=httpx.Response(200,json={'created':0},request=httpx.Request('POST','https://offline.invalid/contacts'))
  with patch('guava.campaigns.httpx.post',return_value=response) as post:
   Campaign(client,'audit','audit','audit').upload_contacts([]);self.assertEqual(post.call_args.kwargs['params']['accepted_terms_of_service'],'false')
 def test_tls_default_rejects_unverified_certificates(self):
  ctx=ssl.create_default_context();self.assertEqual(ctx.verify_mode,ssl.CERT_REQUIRED);self.assertTrue(ctx.check_hostname)
