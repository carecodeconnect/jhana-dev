import wave
import whisper

def transcribe_audio(filename, model_name="tiny.en"):
    # Load the Whisper model and transcribe the audio file
    model = whisper.load_model(model_name)
    result = model.transcribe(filename)
    
    # Print the transcribed text
    print(f"Instruction given by the user: {result['text']}")
    
    return result['text']
