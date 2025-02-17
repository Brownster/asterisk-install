import os
import json
import random
import logging
import time
import unittest
from pathlib import Path
from typing import Tuple, Optional
from dotenv import load_dotenv
from openai import OpenAI
import elevenlabs

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ivr_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
OUTPUT_DIR = Path("/var/lib/asterisk/sounds/ivr_voices")
PERSONAS = {
    "elderly": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "scripts": {
            "greeting": [],
            "confusion": [],
            "compliance": []
        }
    },
    "tech_support": {
        "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
        "scripts": {
            "greeting": [],
            "warning": []
        }
    }
}

class AsteriskIVR:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.persona_state = {}
        self.fallback_persona = "elderly"
        self.fallback_category = "confusion"
        
        # Validate configuration
        self.validate_config()
        self.validate_directory()

    def validate_directory(self):
        if not OUTPUT_DIR.exists():
            logger.critical(f"Output directory {OUTPUT_DIR} does not exist!")
            raise FileNotFoundError(f"Directory {OUTPUT_DIR} not found")
            
    def validate_config(self):
        for persona, config in PERSONAS.items():
            for category, files in config["scripts"].items():
                for f in files:
                    if not Path(f).exists():
                        raise FileNotFoundError(f"Missing audio file: {f}")

    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    response_format="text"
                )
            return transcript.lower()
        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            return None

    def _fallback_response(self, transcript: str) -> Tuple[str, str]:
        available_personas = list(PERSONAS.keys())
        persona = random.choice(available_personas)
        categories = list(PERSONAS[persona]["scripts"].keys())
        category = random.choice(categories)
        return persona, category

    def get_response(self, transcript: str, caller_id: str) -> Optional[str]:
        try:
            transcript = transcript.lower().strip()

            if "credit card" in transcript:
                persona, category = "elderly", "compliance"
            elif "computer" in transcript:
                persona, category = "tech_support", "greeting"
            else:
                persona, category = self._fallback_response(transcript)

            try:
                files = PERSONAS[persona]["scripts"][category]
                chosen_file = random.choice(files)
                
                if not Path(chosen_file).exists():
                    raise FileNotFoundError(f"Missing audio file: {chosen_file}")
                    
                return chosen_file
                
            except KeyError:
                logger.error(f"Invalid persona/category: {persona}/{category}")
                return self._get_emergency_response()
                
        except Exception as e:
            logger.error(f"Response selection error: {str(e)}", exc_info=True)
            return self._get_emergency_response()

    def _get_emergency_response(self) -> Optional[str]:
        emergency_path = OUTPUT_DIR / "system" / "error.wav"
        if emergency_path.exists():
            return str(emergency_path)
        logger.critical("Emergency response file missing!")
        return None

    def handle_call(self, channel):
        try:
            greeting_path = OUTPUT_DIR / "greeting.wav"
            if greeting_path.exists():
                channel.streamFile(str(greeting_path))
            else:
                channel.streamFile(str(self._get_emergency_response()))

            while True:
                try:
                    audio_file = "/tmp/last_input.wav"
                    channel.recordFile(audio_file, "wav", "#", 5000)
                    
                    if transcript := self.transcribe_audio(audio_file):
                        if response := self.get_response(transcript, channel.callerid):
                            channel.streamFile(response)
                            time.sleep(random.uniform(0.8, 1.2))
                    else:
                        channel.streamFile(str(self._get_emergency_response()))
                        
                except IOError as e:
                    logger.error(f"IO error: {str(e)}")
                except Exception as e:
                    logger.error(f"Call handling error: {str(e)}")

        finally:
            channel.hangup()

def generate_voice_files():
    """Generate all audio assets using ElevenLabs API"""
    elevenlabs.set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    
    script_content = {
        "elderly": {
            "greeting": [
                "Hello? Who's calling please?",
                "Oh goodness, the phone actually worked! Hello there!"
            ],
            "confusion": [
                "Could you repeat that? My hearing aid is acting up..."
            ],
            "compliance": ["Let me get my credit card..."]
        },
        "tech_support": {
            "greeting": ["Please press Windows key + R to open remote connection..."],
            "warning": ["I detect a virus on YOUR system!"]
        }
    }

    for persona, config in PERSONAS.items():
        persona_dir = OUTPUT_DIR / persona
        persona_dir.mkdir(parents=True, exist_ok=True)
        
        for category, phrases in script_content[persona].items():
            category_dir = persona_dir / category
            category_dir.mkdir(exist_ok=True)
            
            for idx, phrase in enumerate(phrases):
                output_file = category_dir / f"{idx+1}.wav"
                if output_file.exists():
                    continue
                    
                audio = elevenlabs.generate(
                    text=phrase,
                    voice=config["voice_id"],
                    model="eleven_monolingual_v1"
                )
                
                with open(output_file, "wb") as f:
                    f.write(audio)
                
                PERSONAS[persona]["scripts"][category].append(str(output_file))
                time.sleep(0.5)
    
    # Generate system files
    system_dir = OUTPUT_DIR / "system"
    system_dir.mkdir(exist_ok=True)
    (system_dir / "error.wav").touch()

class TestAsteriskIVR(unittest.TestCase):
    def setUp(self):
        self.ivr = AsteriskIVR()
        self.mock_channel = MockAsteriskChannel()

    def test_keyword_detection(self):
        response = self.ivr.get_response("credit card information", "")
        self.assertIn("elderly/compliance", response)

    def test_fallback_response(self):
        response = self.ivr.get_response("random text", "")
        self.assertTrue(any(p in response for p in PERSONAS.keys()))

class MockAsteriskChannel:
    def __init__(self):
        self.callerid = "UNKNOWN"

    def streamFile(self, file_path):
        logger.info(f"Playing: {file_path}")

    def recordFile(self, path, fmt, term, timeout):
        logger.info(f"Recording to: {path}")

    def hangup(self):
        logger.info("Call terminated")

if __name__ == "__main__":
    # Generate files (first-time setup)
    generate_voice_files()
    
    # Run tests
    unittest.main(argv=[''], exit=False)
    
    # Example usage
    ivr = AsteriskIVR()
    ivr.handle_call(MockAsteriskChannel())
