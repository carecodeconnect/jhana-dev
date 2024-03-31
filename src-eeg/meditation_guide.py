import time
from langchain_community.llms import Ollama
from speaker import generate_speech  # Import the generate_speech function
import shared  # Import the shared module to access the pause_duration variable
import eeg  # Import the eeg module to compute EEG metrics

def initialize_model():
    """Initializes and returns the Ollama model."""
    return Ollama(model="carecodeconnect/jhana-mistral-7b-gguf")

def handle_pause_instruction(pause_instruction, sentences_printed, eeg_stream_inlet, fs):
    """Handles a pause instruction by computing EEG metrics for the specified duration,
    unless no sentences have been printed yet."""
    if not sentences_printed:
        # Skip the pause instruction if no sentences have been printed yet
        return

    try:
        # Update the shared pause_duration
        shared.pause_duration = float(pause_instruction.strip('[]'))
        print(f"Scanning brain waves for {shared.pause_duration} seconds.")

        # Call compute_metrics from eeg.py, which will run for the duration of shared.pause_duration
        eeg.compute_metrics(eeg_stream_inlet, fs)

    except ValueError:
        pass  # Ignore invalid pause instructions

def process_chunk(chunk, in_pause, sentence, pause_buffer):
    """Processes a single chunk of text from the model's output."""
    if '[' in chunk and not in_pause:
        in_pause = True
        pre_pause_text, pause_start = chunk.split('[', 1)
        sentence += pre_pause_text
        pause_buffer += '[' + pause_start
    elif ']' in chunk and in_pause:
        pause_buffer += chunk
        in_pause = False
    elif in_pause:
        pause_buffer += chunk
    else:
        sentence += chunk
    return in_pause, sentence, pause_buffer

def print_sentences_from_buffer(sentence_buffer):
    """Uses TTS to vocalize complete sentences from the sentence buffer and returns any remaining incomplete sentence."""
    sentences = sentence_buffer.split('.')
    for sentence in sentences[:-1]:
        complete_sentence = sentence.strip() + '.'
        generate_speech(complete_sentence)  # Use TTS to vocalize the sentence
    return sentences[-1]

def meditation_guidance(prompt, eeg_stream_inlet, fs):
    """Guides the user through a meditation based on the given prompt, integrating EEG metrics computation during pauses."""
    model = initialize_model()

    sentence_buffer = ""
    pause_buffer = ""
    in_pause = False
    sentences_printed = False  # Flag to track if any sentences have been vocalized

    for chunk in model.stream(prompt):
        in_pause, sentence_buffer, pause_buffer = process_chunk(chunk, in_pause, sentence_buffer, pause_buffer)
        if '.' in chunk:
            sentence_buffer = print_sentences_from_buffer(sentence_buffer)
            sentences_printed = True  # Update flag after vocalizing sentences

        if not in_pause and pause_buffer:
            handle_pause_instruction(pause_buffer, sentences_printed, eeg_stream_inlet, fs)
            pause_buffer = ""

    # Process any remaining text after the loop
    if sentence_buffer:
        print_sentences_from_buffer(sentence_buffer)  # Vocalize any remaining text


