# # speaker.py

# import torch
# from TTS.api import TTS
# import simpleaudio as sa

# # Determine the device based on CUDA availability
# device = 'cuda' if torch.cuda.is_available() else 'cpu'

# # Initialize the TTS object at the module level and move it to the specified device
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# def generate_speech(sentence):
#     # Generate speech from the input sentence and save it to "output.wav"
#     tts.tts_to_file(
#         text=sentence,
#         file_path="output.wav",
#         speaker_wav=["voice-to-clone.wav"],
#         language="en", # for multilingual model
#         split_sentences=True
#     )
#     # Play the generated audio
#     play_audio("output.wav")

# def play_audio(file_path):
#     wave_obj = sa.WaveObject.from_wave_file(file_path)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()
import torch
from TTS.api import TTS
import simpleaudio as sa
import os
from audiostretchy.stretch import stretch_audio  # Import the stretch_audio function from audiostretchy

# Determine the device based on CUDA availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# # Initialize the TTS object with a voice cloning model and move it to the specified device
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)  # or xtts_v1.1

# Initialize the TTS object with a single speaker model and move it to the specified device
tts = TTS("tts_models/en/jenny/jenny", progress_bar=False).to(device)

def generate_speech(sentence):
    # Make sure the audio directory exists
    if not os.path.exists("../audio"):
        os.makedirs("../audio")

    # Generate speech from the input sentence and save it to "../audio/temp_output.wav"
    # Using a temporary output file for the initial TTS output
    temp_output_file = "../audio/temp_output.wav"
    tts.tts_to_file(
        text=sentence,
        file_path=temp_output_file
    )

#     # Check if the input voice file exists
#     voice_file = "../audio/voice-to-clone.wav"
#     if not os.path.isfile(voice_file):
#         raise FileNotFoundError("No voice to clone")

#     # Make sure the audio directory exists
#     if not os.path.exists("audio"):
#         os.makedirs("audio")

#     # Generate speech from the input sentence and save it to "audio/output.wav"
#     output_file = "../audio/output.wav"  # Update the file path to include the audio/ directory
#     tts.tts_to_file(
#         text=sentence,
#         file_path=output_file,  # Updated file path
#         speaker_wav=[voice_file],
#         language="en",  # for multilingual model
#         split_sentences=True
#     )
    
    # Stretch the generated speech and save it to "../audio/output.wav"
    output_file = "../audio/output.wav"
    # Stretch the audio by a certain ratio, adjust the ratio as needed
    stretch_audio(temp_output_file, output_file, ratio=1.25)

    # Play the stretched audio
    play_audio(output_file)

    # Optionally, remove the temp_output_file after the process is complete
    os.remove(temp_output_file)

def play_audio(file_path):
    # Ensure the output audio file exists before attempting to play it
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Output audio file not found")

    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()
