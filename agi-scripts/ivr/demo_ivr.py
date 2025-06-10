#!/usr/bin/env python3
from asterisk.agi import AGI
from allowed_callers import load_allowed_callers, load_owner_callers
from llm.llm_client import LLMClient
from stt.azure_stt import recognize_speech_from_file
from tts.azure_tts import synthesize_speech_to_file


GREETING_OWNER = "Hello owner, how can I assist you?"
GREETING_ALLOWED = "Hello, how may we help you today?"
GREETING_UNKNOWN = "Please state your request after the beep."


def main():
    agi = AGI()
    caller = agi.env.get("agi_callerid", "UNKNOWN")
    agi.verbose(f"Incoming call from {caller}", 3)

    owners = load_owner_callers()
    allowed = load_allowed_callers()

    if caller in owners:
        greeting = GREETING_OWNER
    elif caller in allowed:
        greeting = GREETING_ALLOWED
    else:
        greeting = GREETING_UNKNOWN

    greet_file = "/tmp/greet.wav"
    synthesize_speech_to_file(greeting, greet_file)
    agi.stream_file(greet_file.rstrip(".wav"))

    record_file = "/tmp/record.wav"
    agi.record_file(record_file.rstrip(".wav"), "wav", "#", 5000)
    text = recognize_speech_from_file(record_file)
    response = LLMClient().get_response(text).get("text", "")
    resp_file = "/tmp/resp.wav"
    synthesize_speech_to_file(response, resp_file)
    agi.stream_file(resp_file.rstrip(".wav"))
    agi.hangup()


if __name__ == "__main__":
    main()
