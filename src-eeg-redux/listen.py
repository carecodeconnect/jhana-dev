from pysilero_vad import SileroVoiceActivityDetector
import pyaudio
from recorder import Recorder
import sys

def monitor_audio_stream(pre_buffer_duration=3, vad_threshold=0.5, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000):
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    vad = SileroVoiceActivityDetector()

    pre_buffer_frames = int(pre_buffer_duration * rate / chunk_size)
    pre_buffer = []

    print("Monitoring for voice activity...")
    dot_count = 0
    while True:
        audio_data = stream.read(chunk_size)
        audio_bytes = audio_data

        pre_buffer.append(audio_data)
        if len(pre_buffer) > pre_buffer_frames:
            pre_buffer.pop(0)

        if vad(audio_bytes) >= vad_threshold:
            print("\nVoice detected!")
            stream.stop_stream()
            stream.close()
            audio_interface.terminate()
            return pre_buffer

        sys.stdout.write('\r' + '.' * (dot_count % 10))  # Print dots in place, cycling every 10 iterations
        sys.stdout.flush()
        dot_count += 1

    return None

def start_recording_if_voice_detected():
    pre_buffered_frames = monitor_audio_stream()

    if pre_buffered_frames is not None:
        recorder = Recorder()
        recorder.record_audio_with_prebuffer(pre_buffered_frames, duration=5)
        print(f"Recording saved as {recorder.filename}")
