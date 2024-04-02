import listen  # Module for voice activity detection and initiating recording
import meditation_guide  # Module for meditation guidance using TTS
from recorder import Recorder
# Assuming Whisper is used for transcription, we no longer use the original transcriber module
import whisper
import eeg  # Import the EEG module to access the neurofeedback functions
import torch
import gc

def load_whisper_model(model_name="small.en"): # tiny.en small.en medium.en
    """
    Load the specified Whisper model.

    Parameters:
    - model_name: The name of the Whisper model to load.

    Returns:
    - The loaded Whisper model.
    """
    model = whisper.load_model(model_name)
    return model

def transcribe_audio_with_whisper(filename, model):
    """
    Transcribe audio using the Whisper model.

    Parameters:
    - filename: Filename of the audio to transcribe.
    - model: The loaded Whisper model.

    Returns:
    - The transcribed text of the recorded audio.
    """
    result = model.transcribe(filename)
    transcription = result["text"]
    return transcription

def audio_recording_and_transcription(filename="../audio/recorded_audio.wav"):
    """
    Record audio after voice activity detection and transcribe it using Whisper.

    Parameters:
    - filename: Filename to save the recorded audio.

    Returns:
    - The transcribed text of the recorded audio.
    """
    # Use the Recorder class to record audio after voice is detected
    recorder = Recorder(filename=filename)
    recorder.record_audio(duration=5)  # Record for 5 seconds

    # Load the Whisper model
    whisper_model = load_whisper_model()

    # Transcribe the recorded audio using Whisper
    transcription = transcribe_audio_with_whisper(recorder.filename, whisper_model)
    print(f"Transcribed Text: {transcription}")
    return transcription

def main():
    torch.cuda.empty_cache()  # Clear CUDA cache before starting a GPU-intensive task
    gc.collect()  # Force garbage collection to free up memory
    
    # Initialize the EEG stream
    inlet = eeg.initialize_stream()
    if inlet is None:
        print("Could not initialize the EEG stream. Please check the connection.")
        return  # Exit if the EEG stream could not be initialized

    # Get the sampling frequency from the inlet's info
    fs = int(inlet.info().nominal_srate())

    # Wait for voice activity before starting the recording
    listen.start_recording_if_voice_detected()  # This will record audio including pre-buffer when voice is detected

    # Transcribe the recorded audio using Whisper
    whisper_model = load_whisper_model()
    transcribed_prompt = transcribe_audio_with_whisper("../audio/recorded_audio.wav", whisper_model)  # Use the default filename from Recorder

    if transcribed_prompt:
        # Use the transcribed text as the prompt for meditation guidance, passing the inlet and fs
        meditation_guide.meditation_guidance(transcribed_prompt, inlet, fs)
    else:
        print("No transcription available.")

if __name__ == "__main__":
    main()
    # Final cleanup
    torch.cuda.empty_cache()
    gc.collect()
