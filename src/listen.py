from pysilero_vad import SileroVoiceActivityDetector
import pyaudio
from recorder import Recorder

def monitor_audio_stream(pre_buffer_duration=3, vad_threshold=0.5, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000):
    """
    Continuously monitor the audio stream for voice activity. Include a pre-buffer to capture audio before detection.

    Parameters:
    - pre_buffer_duration: Duration of the audio pre-buffer in seconds.
    - vad_threshold: Threshold for voice activity detection.
    - chunk_size: The size of audio chunks to read at a time.
    - format: The sample format.
    - channels: The number of channels.
    - rate: The sampling rate.

    Returns:
    - A list of pre-buffered frames if voice is detected, otherwise None.
    """
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    vad = SileroVoiceActivityDetector()

    # Pre-buffer to store a few seconds of audio
    pre_buffer_frames = int(pre_buffer_duration * rate / chunk_size)
    pre_buffer = []

    print("Monitoring for voice activity...")
    while True:
        audio_data = stream.read(chunk_size)
        audio_bytes = audio_data

        # Maintain pre-buffer
        pre_buffer.append(audio_data)
        if len(pre_buffer) > pre_buffer_frames:
            pre_buffer.pop(0)

        # Check for voice activity
        if vad(audio_bytes) >= vad_threshold:
            print("Voice detected!")
            stream.stop_stream()
            stream.close()
            audio_interface.terminate()
            return pre_buffer  # Return the pre-buffered frames

        print("Listening...")

    return None

def start_recording_if_voice_detected():
    pre_buffered_frames = monitor_audio_stream()

    if pre_buffered_frames is not None:
        # Voice detected, start recording including pre-buffered frames
        recorder = Recorder()
        recorder.record_audio_with_prebuffer(pre_buffered_frames, duration=5)  # This function needs to be added to Recorder class
        print(f"Recording saved as {recorder.filename}")
