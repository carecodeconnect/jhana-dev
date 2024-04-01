#!/usr/bin/env python
import listen  # Module for voice activity detection and initiating recording
import meditation_guide  # Module for meditation guidance using TTS
from recorder import Recorder
import whisper
import gc  # Import garbage collector
from transcriber import transcribe_audio

def load_whisper_model(model_name="medium.en"): # tiny.en base.en small.en medium.en
    """
    Load the Whisper model.

    Parameters:
    - model_name: The name of the Whisper model to load.

    Returns:
    - The loaded Whisper model.
    """
    return whisper.load_model(model_name)

def audio_recording_and_transcription(model, filename="../audio/recorded_audio.wav"):
    """
    Record audio after voice activity detection, transcribe it using the given Whisper model.

    Parameters:
    - model: The loaded Whisper model to use for transcription.
    - filename: Filename to save the recorded audio.

    Returns:
    - The transcribed text of the recorded audio.
    """
    recorder = Recorder(filename=filename)
    recorder.record_audio(duration=5)  # Record for 5 seconds

    transcription = transcribe_audio(recorder.filename, model)
    print(f"Transcribed Text: {transcription}")
    return transcription

def main():
    # Load the Whisper model
    model = load_whisper_model()

    # Wait for voice activity before starting the recording
    listen.start_recording_if_voice_detected()  # This will record audio including pre-buffer when voice is detected

    # Transcribe the recorded audio using the loaded model
    transcribed_prompt = transcribe_audio("../audio/recorded_audio.wav", model)  # Use the default filename from Recorder

    if transcribed_prompt:
        meditation_guide.meditation_guidance(transcribed_prompt)
    else:
        print("No transcription available.")

    # Clear the Whisper model from memory
    del model
    gc.collect()  # Explicitly invoke garbage collection

if __name__ == "__main__":
    main()

