import pyaudio
import wave

class Recorder:
    def __init__(self, filename="recorded_audio.wav"):
        self.filename = filename
        self.format = pyaudio.paInt16  # 16-bit resolution
        self.channels = 1  # mono
        self.rate = 16000  # sample rate
        self.chunk = 1024  # buffer size
        self.audio = pyaudio.PyAudio()

    def record_audio_with_prebuffer(self, pre_buffered_frames, duration=5):
        print("Recording with pre-buffer...")
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        frames = list(pre_buffered_frames)  # Include pre-buffered frames in the recording

        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("Recording ended.")
        stream.stop_stream()
        stream.close()
        self.save_audio(frames)

    def save_audio(self, frames):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Audio saved as {self.filename}")
