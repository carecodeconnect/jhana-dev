# speaker.py

import torch
from TTS.api import TTS
import simpleaudio as sa

# Determine the device based on CUDA availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize the TTS object at the module level and move it to the specified device
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def generate_speech(sentence):
    # Generate speech from the input sentence and save it to "output.wav"
    tts.tts_to_file(
        text=sentence,
        file_path="output.wav",
        speaker_wav=["voice-to-clone.wav"],
        language="en", # for multilingual model
        split_sentences=True
    )
    # Play the generated audio
    play_audio("output.wav")

def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

