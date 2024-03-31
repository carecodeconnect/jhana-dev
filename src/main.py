# Import necessary modules
import listen  # Module for voice activity detection and initiating recording
import meditation_guide  # Module for meditation guidance using TTS
from recorder import Recorder
from transcriber import transcribe_audio

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
    # Wait for voice activity before starting the recording
    listen.start_recording_if_voice_detected()  # This will record audio including pre-buffer when voice is detected

    # Transcribe the recorded audio
    transcribed_prompt = transcribe_audio("recorded_audio.wav")  # Use the default filename from Recorder

    if transcribed_prompt:
        # Use the transcribed text as the prompt for meditation guidance
        meditation_guide_speaker.meditation_guidance(transcribed_prompt)
    else:
        print("No transcription available.")

if __name__ == "__main__":
    main()

