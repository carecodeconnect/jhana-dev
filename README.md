# `Jhāna.AI`: Personal Meditation Guide :pray:

`Jhāna.AI` is an interactive voice assistant which uses real-time brain sensing to guide the user in ancient Jhana Meditation, for reaching states of concentration, bliss and calm, and finding relief from pain. `Jhāna.AI` uses cutting-edge technologies of biofeedback, deep learning, and natural language processing for personalised guided meditation sessions. 

## Background

The heart of `Jhāna.AI` is the language model `jhana-mistral-7b-gguf`. This model is trained on a large corpus of meditation texts, and is fine-tuned on a smaller dataset of meditation instructions. The model is capable of generating novel meditation instructions, and can be used to guide the user in a meditation session. The model is deployed with `ollama`, and is accessed by the `Jhana` app.

For a summary of the project, see [Jhana Project Summary](docs/jhana-project-summary.md).

## Requirements

- NVIDIA/AMD GPU with CUDA support is recommended for running the deep learning models.
- 8 GB of VRAM is recommended.
- A microphone is required for voice input.
- A Muse EEG headband is required for brain sensing.
- A Windows/Linux/MacOS machine is required for running the app.
- Around 20 GB of free disk space is required for the deep learning models.
- Python 3.10 is recommended.

## Installation

On first running the app, the deep learning models will be downloaded and installed. This may take some time, depending on your internet connection. An alternative is to download the models prior to running the app, by running the following commands:

### Prerequisites: Ubuntu Users

- `sudo apt install gcc` # for simpleaudio
- `sudo apt install ffmpeg`
- `sudo apt install pulseaudio`
- `sudo apt install libpcap-dev`
- `sudo apt install python3-dev`
- `sudo setcap 'cap_net_raw,cap_net_admin=eip' $(which hcitool)`

### Install Ollama

[Download Ollama](https://ollama.com/download), which should automatically start the ollama service.

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

### Install Conda Packages

- `conda install -c conda-forge PyAudio=0.2.14`
- `conda install alsa-plugins` # for Ubuntu

### Install TTS

- `pip install TTS`

To run tts in the terminal and download the model for the first time:
```
 tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
     --text "Bugün okula gitmek istemiyorum." \
     --speaker_wav /path/to/target/speaker.wav \
     --language_idx tr \
     --use_cuda true
```

For further information on TTS, see [TTS Documentation](https://docs.coqui.ai/en/latest/models/xtts.html).

### EEG with Muse

- `pip install muselsl`

## Usage

1. Change directory: `cd src`

2. Run the app: `python main.py`

3. Jhana will wait for your voice with a "Listening..." prompt

4. Say "Guide me in a loving-kindness meditation" to begin the meditation session!