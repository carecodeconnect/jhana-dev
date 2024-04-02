import wave
import whisper
import gc
import torch

def transcribe_audio(filename, model_name="small.en"): #  tiny.en or small.en or medium.en
    # Load the Whisper model and transcribe the audio file
    model = whisper.load_model(model_name)
    result = model.transcribe(filename)
    
    del model  # done with the model
    torch.cuda.empty_cache()
    gc.collect()

    # Print the transcribed text
    print(f"Instruction given by the user: {result['text']}")
    
    return result['text']
