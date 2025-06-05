import speech_recognition as sr
import pyttsx3
import time

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = self._init_tts()
        
    def _init_tts(self):
        """Initialize text-to-speech with fallbacks"""
        try:
            return pyttsx3.init()
        except Exception:
            print("Warning: TTS initialization failed - voice output disabled")
            return None
    
    def listen(self):
        """Listen to microphone with robust error handling"""
        try:
            with sr.Microphone() as source:
                print("\n🔴 Listening...", end="", flush=True)
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=30)
                
                print("\r🟢 Processing...", end="", flush=True)
                text = self.recognizer.recognize_google(audio).lower()
                print("\r" + " " * 30 + "\r", end="")  # Clear line
                return text
                
        except sr.WaitTimeoutError:
            print("\r❌ No speech detected", end="", flush=True)
            return ""
        except Exception as e:
            print(f"\r⚠️ Voice error: {str(e)[:50]}...", end="", flush=True)
            return ""

    def speak(self, text):
        """Speak text if TTS is available"""
        if self.engine and text:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass  # Silent fail for voice errors