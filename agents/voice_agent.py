import speech_recognition as sr
from gtts import gTTS
import os
import uuid

class VoiceAgent:
    def __init__(self):
        """
        Initialize Voice Agent for STT and TTS.
        """
        self.recognizer = sr.Recognizer()

    def speech_to_text(self):
        """
        Convert speech to text using microphone input.
        Returns:
            str: Transcribed text or None if failed.
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            print("Voice Agent: Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Voice Agent STT error: {e}")
            return None

    def text_to_speech(self, text, output_file=None):
        """
        Convert text to speech and save as MP3.
        Args:
            text (str): Text to convert to speech.
            output_file (str): Path to save audio file (optional).
        Returns:
            str: Path to saved audio file or None if failed.
        """
        try:
            if not output_file:
                output_file = f"response_{uuid.uuid4()}.mp3"
            tts = gTTS(text=text, lang="en")
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Voice Agent TTS error: {e}")
            return None

    def cleanup(self, audio_file):
        """
        Remove temporary audio file.
        Args:
            audio_file (str): Path to audio file.
        """
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
        except Exception as e:
            print(f"Voice Agent cleanup error: {e}")

if __name__ == "__main__":
    agent = VoiceAgent()
    # Test STT
    text = agent.speech_to_text()
    if text:
        print("Transcribed Text:", text)
    # Test TTS
    sample_text = "This is a test response."
    audio_file = agent.text_to_speech(sample_text)
    if audio_file:
        print(f"Audio saved to: {audio_file}")
        agent.cleanup(audio_file)