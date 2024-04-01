# `Jhāna.AI`: Personal Meditation Guide :pray:

`Jhāna.AI` is an interactive voice assistant which uses real-time brain sensing to guide the user in ancient Jhana Meditation, for reaching states of concentration, bliss and calm, and finding relief from pain. `Jhāna.AI` uses cutting-edge technologies of biofeedback, deep learning, and natural language processing for personalised guided meditation sessions. 

![Jhana.AI](img/jhana-logo.webp)

## Background

The heart of `Jhāna.AI` is the language model [jhana-mistral-7b-gguf](https://ollama.com/carecodeconnect/jhana-mistral-7b-gguf). This model is trained on a large corpus of meditation texts, and is fine-tuned on a smaller dataset of meditation instructions. The model is capable of generating novel meditation instructions, and can be used to guide the user in a meditation session. The model is deployed with `ollama`, and is accessed by the `Jhana` app.

For a summary of the project, see [Jhana Project Summary](docs/jhana-project-summary.md).

To download the model from Hugging Face, see [jhana-mistral-GGUF](https://huggingface.co/carecodeconnect/jhana-mistral-GGUF).

## Requirements

- Windows/MacOS/Linux machine with at least i5 or equivalent processor.
- NVIDIA/AMD GPU with CUDA support recommended for running the deep learning models.
- 8 GB of VRAM is recommended.
- Around 20 GB of free disk space is required for the deep learning models.
- Python 3.10 is recommended.
- Microphone is required for voice input.
- [Muse 2](https://choosemuse.com/products/muse-2) EEG headband is required for the brain sensing option (optional).

## Installation

On first running the app, the deep learning models will be downloaded and installed. This may take some time, depending on your internet connection. An alternative is to download the models prior to running the app, by running the following commands:

### Prerequisites

#### Windows

Install Chocolatey by following these instructions: [here](https://chocolatey.org/install) or [here](https://community.chocolatey.org/courses/installation/installing?method=installing-chocolatey).

Run Command Prompt (`cmd.exe`) or PowerShell (`powershell.exe`) as Administrator and install the following packages:

- `choco install ffmpeg`

#### MacOS

- `brew install ffmpeg`

#### Ubuntu

- `sudo apt install gcc` # for simpleaudio
- `sudo apt install ffmpeg`
- `sudo apt install pulseaudio`
- `sudo apt install libasound2-plugins`
- `sudo apt install alsa-base`
- `sudo apt install alsa-utils`
- `sudo apt install alsa-oss`
- `sudo apt install libasound2`
- `sudo apt install libasound2-dev`
- `sudo apt install libpcap-dev`
- `sudo apt install python3-dev`
- `sudo setcap 'cap_net_raw,cap_net_admin=eip' $(which hcitool)`

### Install Ollama

[Download Ollama](https://ollama.com/download), and install it for your operating system, which should automatically start the ollama service.

- `ollama pull carecodeconnect/jhana-mistral-7b-gguf` will download the model.

### Create Conda Environment

- `conda create -n jhana python=3.10`

### Activate Conda Environment: 

- `conda activate jhana`

### Clone the Repository

- `git clone https://github.com/carecodeconnect/jhana-dev`

### Navigate to `jhana-dev` Directory: 

- `cd jhana-dev`

### Install Dependencies

- `pip install -r requirements.txt`

### Install PyAudio

Follow the instructions at [PyAudio](https://pypi.org/project/PyAudio/)

For example:

#### Windows

- `pip install pyaudio==0.2.14`

#### MacOS

- `brew install portaudio` then `pip install pyaudio==0.2.14`

#### Ubuntu

- `conda install -c conda-forge PyAudio=0.2.14`
- `conda install alsa-plugins`

### Install Whisper and Download Model

Follow the instructions at [OpenAI Whisper](https://pypi.org/project/openai-whisper/). For example:

- `pip install openai-whisper==20231117`

To download a speech-to-text model for the first time:

- `cd audio`
- `whisper voice-to-clone.wav --language English --model small.en` 

This should create several transcriptions as text files in the current directory.

For further information on Whisper, see [openai-whisper](https://pypi.org/project/openai-whisper/).

### Install TTS and Download Model

- `pip install TTS` # if not already installed

To run `tts` in the terminal and download the text-to-speech model for the first time, check you are still in the `audio` folder, then:

#### Windows:

To use CUDA, set `--use_cuda true`, or `--use_cuda false` for CPU.

`tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --text "Focus on your breath." --speaker_wav voice-to-clone.wav --language_idx en --use_cuda true`

#### MacOS or Ubuntu:

To use CUDA, set `--use_cuda true`, or `--use_cuda false` for CPU.

```
 tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
     --text "Focus on your breath." \
     --speaker_wav voice-to-clone.wav \
     --language_idx en \
     --use_cuda true
```

To play the recorded audio:

##### Windows:

- `start tts_output.wav`

##### MacOS:

- `afplay tts_output.wav`

##### Ubuntu:

- `aplay tts_output.wav` or `cvlc --play-and-exit tts_output.wav`

The `tts` models suitable for voice cloning are `tts_models/multilingual/multi-dataset/xtts_v2` and `tts_models/multilingual/multi-dataset/xtts_v1.1`.

For further information on TTS, see [TTS Documentation](https://docs.coqui.ai/en/latest/models/xtts.html).

### EEG with Muse

In addition to the above, the following packages are required for EEG sensing with Muse:

- `pip install -r requirements-eeg.txt`

Or install the packages individually:

- `pip install muselsl==2.2.2`
- `pip install pylsl==1.16.2`
- `pip install playsound==1.3.0`
- `pip install matplotlib==3.8.2`
- `pip install numpy==1.25.2`
- `pip install scikit-learn==1.4.0`
- `pip install scipy==1.4.0`

## Usage

Jhana can be run in two modes: with or without EEG sensing. The EEG sensing mode requires a Muse 2 EEG headband.

1. Navigate to the `src` directory:

`cd ..`


2. Run the app: 

- `python main.py`

Or:

### MacOS or Ubuntu

- `./main.py`

3. Jhana will wait for your voice with a "Listening..." prompt

4. Say "Guide me in a loving-kindness meditation" to begin the meditation session!

To run the app with EEG sensing:

0. Ensure that the Muse 2 EEG headband is connected to the computer via Bluetooth.

1. Change directory: `cd src-eeg`

2. Run the app: `python main.py`

3. Jhana will wait for your voice with a "Listening..." prompt

4. Say "Guide me in a loving-kindness meditation" to begin the meditation session!