import torch
from TTS.api import TTS
import simpleaudio as sa
import os
# Assuming the stretch_audio function is available from the audiostretchy library
from audiostretchy.stretch import stretch_audio

# Set the device to cuda or cpu
device = 'cuda'

# Initialize the TTS object with Jenny model and move it to the device
tts = TTS("tts_models/en/jenny/jenny", progress_bar=False).to(device)

def generate_speech(sentence):
    # Ensure the audio directory exists
    if not os.path.exists("../audio"):
        os.makedirs("../audio")

    # Path for the output audio file
    output_file = "../audio/output.wav"

    # Generate speech from the input sentence and save it directly to "audio/output.wav"
    tts.tts_to_file(
        text=sentence,
        file_path=output_file,  # Directly specifying the output path
    )

    # Stretch the audio
    stretch_ratio = 1.25  # Define your desired stretch ratio here
    stretch_audio(output_file, output_file, ratio=stretch_ratio)  # Assuming in-place stretching is supported

    # Play the stretched audio
    play_audio(output_file)

def play_audio(file_path):
    # Ensure the output audio file exists before attempting to play it
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Output audio file not found")

    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# import torch
# from TTS.api import TTS
# import simpleaudio as sa
# import os

# # Set the device to CPU
# device = 'cpu'

# # Initialize the TTS object with a voice cloning model and move it to the CPU
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# def generate_speech(sentence):
#     # Define output file paths
#     audio_dir = "../audio"
#     output_file = os.path.join(audio_dir, "output.wav")
#     voice_file = os.path.join(audio_dir, "voice-to-clone.wav")

#     # Make sure the audio directory exists
#     if not os.path.exists(audio_dir):
#         os.makedirs(audio_dir)

#     # Check if the input voice file exists
#     if not os.path.isfile(voice_file):
#         raise FileNotFoundError("No voice to clone")

#     # Generate speech from the input sentence and save it to "audio/output.wav"
#     tts.tts_to_file(
#         text=sentence,
#         file_path=output_file,
#         speaker_wav=[voice_file],
#         language="en",  # for multilingual model
#         split_sentences=True
#     )
    
#     # Play the generated audio
#     play_audio(output_file)

# def play_audio(file_path):
#     # Ensure the output audio file exists before attempting to play it
#     if not os.path.isfile(file_path):
#         raise FileNotFoundError("Output audio file not found")

#     wave_obj = sa.WaveObject.from_wave_file(file_path)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()
