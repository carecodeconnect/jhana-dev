# import wave
# import whisper

# def transcribe_audio(filename, model_name="medium.en"): # tiny.en or small.en or medium.en
#     """
    
#     """
    
#     # Load the Whisper model and transcribe the audio file
#     model = whisper.load_model(model_name)
#     result = model.transcribe(filename)
    
#     # Print the transcribed prompt
#     print(f"Instruction given by the user: {result['text']}")
    
#     return result['text']
import wave

def transcribe_audio(filename, model):
    """
    Transcribe the given audio file using the provided Whisper model.

    Parameters:
    - filename: The path to the audio file to transcribe.
    - model: The loaded Whisper model to use for transcription.

    Returns:
    - The transcribed text of the audio.
    """
    
    result = model.transcribe(filename)
    
    print(f"Instruction given by the user: {result['text']}")
    
    return result['text']
