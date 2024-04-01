import torch
from TTS.api import TTS
import simpleaudio as sa
import os

# Determine the device based on CUDA availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize the TTS object at the module level and move it to the specified device
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)  # or xtts_v1.1

def generate_speech(sentence):
    # Check if the input voice file exists
    voice_file = "../audio/voice-to-clone-batman.wav"
    if not os.path.isfile(voice_file):
        raise FileNotFoundError("No voice to clone")

    # Make sure the audio directory exists
    if not os.path.exists("audio"):
        os.makedirs("audio")

    # Generate speech from the input sentence and save it to "audio/output.wav"
    output_file = "../audio/output.wav"  # Update the file path to include the audio/ directory
    tts.tts_to_file(
        text=sentence,
        file_path=output_file,  # Updated file path
        speaker_wav=[voice_file],
        language="en",  # for multilingual model
        split_sentences=True
    )
    # Play the generated audio
    play_audio(output_file)  # Pass the updated file path to the play_audio function

def play_audio(file_path):
    # Ensure the output audio file exists before attempting to play it
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Output audio file not found")

    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

