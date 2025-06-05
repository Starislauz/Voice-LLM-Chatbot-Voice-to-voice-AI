from gemini_brain import GeminiBrain
from voice_interface import VoiceInterface
import sys

import pvporcupine
import pyaudio
import numpy as np

class VoiceChatbot:
    def __init__(self):
        self.ai = GeminiBrain()
        self.voice = VoiceInterface()
        self.running = True
        self.porcupine = pvporcupine.create(
        access_key="peWXboexGaLX/2ONgUCMGSx01QkSaOuetNSMhAcBjxaRftBMikmuQw==",  # <-- paste your key here
        keywords=["americano"]) 
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

    def run(self):
        print("\n🌟 Gemini Voice Assistant 🌟")
        print("Say 'Hey Google' to activate | CTRL+C to quit\n")
        while self.running:
            try:
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = np.frombuffer(pcm, dtype=np.int16)
                result = self.porcupine.process(pcm)
                if result >= 0:
                    print("🔊 Wake word detected!")
                    self.process_voice_input()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                self.running = False
            except Exception as e:
                print(f"\n🔥 Critical error: {e}")
                self.running = False

    def process_voice_input(self):
        """Handle full voice interaction cycle"""
        user_input = self.voice.listen()
        if not user_input:
            return
            
        print(f"\n👤 YOU: {user_input}")
        print("🧠 AI is thinking...", end="", flush=True)
        
        response = self.ai.ask(user_input)
        print("\r" + " " * 30 + "\r", end="")  # Clear line
        
        print(f"🤖 AI: {response}")
        self.voice.speak(response)

if __name__ == "__main__":
    try:
        chatbot = VoiceChatbot()
        chatbot.run()
    except Exception as e:
        print(f"🚨 Failed to start: {e}")
        sys.exit(1)