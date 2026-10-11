# Architecture learning notes
Conceptual pipeline supplied by the user:
Speech -> network/PSTN/WebRTC -> VAD/endpointing -> ASR -> transcript -> conversation/task state -> LLM/business APIs -> response text -> TTS -> audio transport -> listener.
This is a testing model, not a verified description of every Guava internal implementation.

The retrieved official Guava starter describes a hosted Dialog System and Python Expert connected by WebSocket. Agent registers synchronous callbacks; Call commands steer Tasks and Fields. Version-specific transport, errors and testing behavior still require study.
ASR failures mishear input; authorization failures disclose or act without permission; workflow failures choose the wrong next step. A single bad call can contain more than one category.
A mock isolates deterministic behavior but does not prove hosted behavior. Text tests isolate workflow outcomes but omit acoustic and transport behavior. Audio tests need reference transcripts and action traces, not subjective impressions alone.
Documentation describes Agent.test as a LIVE test session: do not assume an SDK testing interface is offline or free merely because it is named test.
Current source: https://goguava.ai/docs/coding-agent-starter.md; locally preserved 2026-10-11 snapshot. No SDK API was invoked this milestone.
