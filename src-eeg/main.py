# Import necessary modules
import listen  # Module for voice activity detection and initiating recording
import meditation_guide_speaker
from recorder import Recorder
from transcriber import transcribe_audio
import eeg  # Import the EEG module to access the neurofeedback functions
import torch
import gc

def audio_recording_and_transcription(filename="recorded_audio.wav"):
    """
    Record audio after voice activity detection and transcribe it.

    Parameters:
    - filename: Filename to save the recorded audio.

    Returns:
    - The transcribed text of the recorded audio.
    """
    # Use the Recorder class to record audio after voice is detected
    recorder = Recorder(filename=filename)
    recorder.record_audio(duration=5)  # Record for 5 seconds

    # Transcribe the recorded audio
    transcription = transcribe_audio(recorder.filename)
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

    # Transcribe the recorded audio
    transcribed_prompt = transcribe_audio("recorded_audio.wav")  # Use the default filename from Recorder

    if transcribed_prompt:
        # Use the transcribed text as the prompt for meditation guidance, passing the inlet and fs
        meditation_guide_speaker.meditation_guidance(transcribed_prompt, inlet, fs)
    else:
        print("No transcription available.")

if __name__ == "__main__":
    main()
    # Final cleanup
    torch.cuda.empty_cache()
    gc.collect()

