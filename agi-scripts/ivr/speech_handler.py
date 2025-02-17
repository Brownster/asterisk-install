from stt.azure_stt import recognize_speech_from_file
from tts.azure_tts import synthesize_speech_to_file

def process_speech(audio_file):
    try:
        recognized_text = recognize_speech_from_file(audio_file)
        return recognized_text
    except Exception as e:
        raise Exception(f"Error processing speech: {e}")

def synthesize_response(text, output_file):
    try:
        return synthesize_speech_to_file(text, output_file)
    except Exception as e:
        raise Exception(f"Error synthesizing speech: {e}")
