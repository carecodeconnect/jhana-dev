import tkinter as tk
from tkinter import scrolledtext
import threading
import sys

# Assuming the imports for your meditation guide modules are here
import listen
import meditation_guide
from recorder import Recorder
from transcriber import transcribe_audio
import eeg
import torch
import gc
from speaker import generate_speech

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Jhana: Personal Meditation Guide")

# Create a scrolled text widget for output with specified background and font
scrolled_text = scrolledtext.ScrolledText(root, width=100, height=30, bg="black", fg="white", font=("Consolas", 25))
scrolled_text.pack()
scrolled_text.configure(state='disabled')  # Start with the widget in the disabled state so it's read-only

class StdoutRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, string)
        self.widget.configure(state='disabled')
        self.widget.yview(tk.END)

    def flush(self):
        pass

# Redirect sys.stdout and sys.stderr to the text widget
sys.stdout = StdoutRedirector(scrolled_text)
sys.stderr = StdoutRedirector(scrolled_text)

def audio_recording_and_transcription(filename="recorded_audio.wav"):
    """
    Record audio after voice activity detection and transcribe it.

    Parameters:
    - filename: Filename to save the recorded audio.

    Returns:
    - The transcribed text of the recorded audio.
    """
    recorder = Recorder(filename=filename)
    transcription = transcribe_audio(recorder.filename)
    print(f"Transcribed Text: {transcription}")
    return transcription

def main_logic():
    """
    Main logic for the meditation guide application.
    """
    torch.cuda.empty_cache()
    gc.collect()

    generate_speech("Hi, I'm Jhana, your meditation guide! What meditation would you like to practice?")
    
    inlet = eeg.initialize_stream()
    if inlet is None:
        print("Could not initialize the EEG stream. Please check the connection.")
        return

    fs = int(inlet.info().nominal_srate())

    listen.start_recording_if_voice_detected()

    transcribed_prompt = transcribe_audio("recorded_audio.wav")
    if transcribed_prompt:
        meditation_guide.meditation_guidance(transcribed_prompt, inlet, fs)
    else:
        print("No transcription available.")

    generate_speech("Thank you for meditating with me!")

    torch.cuda.empty_cache()
    gc.collect()

def main():
    threading.Thread(target=main_logic).start()
    root.mainloop()

if __name__ == "__main__":
    main()
