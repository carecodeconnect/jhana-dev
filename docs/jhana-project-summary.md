# Jhāna AI

# Project Summary

## Overview

Jhāna AI is a cutting-edge conversational agent which provides voice assistance to guide the user in meditation. 

- Multi-modal assistant allowing text or speech interaction with brain-sensing to provide real-time feedback to the user during meditation.

- Trained on a dataset of expert-level guided Jhāna meditations, and uses an EEG brain sensing headband (Muse 2) to monitor the user's meditation state and provide feedback in real-time. 

- Provides personalised expert-level guided meditations, answers questions about meditation, and provides feedback on the user's meditation state.

## Problem Statement

- Chronic pain and stress are two of the most common health problems in the world. Meditation is a potential remedy for these problems, but many people find it difficult to get started with meditation. Our age is characterized by a high level of distraction.Even experienced meditators can struggle to maintain a consistent practice.

- Meditation apps are popular, but they are limited in their ability to provide personalised voice-assistance and interactive feedback to the user. They can provide guided meditations, but they cannot provide real-time feedback on the user's meditation state. This makes it difficult for the user to know if the instructions are suitable for their condition, and difficult to sustain attention and focus during meditation.

- The most commonly taught meditations in the West are mindfulness and relaxation meditations. However, there are other types of meditation that are more effective for treating chronic pain and stress, such as Jhāna meditation. Jhāna meditation is a type of meditation that is designed to produce deep states of concentration and tranquility. But these states are difficult to achieve without guidance, are rarely taught in the West, except in Buddhist and Hindu retreat settings. They are not widely accessible to the general public.

## Our Solution

- They are difficult to achieve without guidance, are rarely taught in the West, except in Buddhist and Hindu retreat settings. They are not widely accessible to the general public.


- Jhāna AI can provide guidance to the user to help them achieve jhāna states. can provide guided meditations, answer questions about meditation, and provide feedback on the user's meditation state. It can also provide real-time feedback on the user's meditation state using an EEG brain sensing headband (Muse 2). Ask Jhāna with text or speech to guide you through a meditation, and it will provide real-time feedback on your meditation state, and help you to achieve deep states of meditation.

## Tech Stack

### Baseline

- Automated Speech Recognition (ASR) for converting user speech to text (OpenAI Whisper)
- LLM (Language Model): trained on a curated dataset of guided jhāna meditations, for understanding user intent and generating responses. Hosted locally with `ollama` (e.g. Microsoft Phi 2, llama2, Mistral, Mixtral, stablelm2) or cloud-based with OpenAI (e.g. GPT-3.5, GPT-4).
- EEG (brainwave) sensing headband (Muse 2) for monitoring user's meditation state.
- `LangChain` for managing the multi-modal conversational agent and providing Retrieval Augmented Generation (RAG) for generating responses from database and web sources of texts.
- Text-To-Speech (TTS) for converting the assistant's responses to speech with voice cloning (Coqui `XTTS-v2`)
- `Docker` for containerization of development environment, to allow for easy collaboration and deployment, including sharing GPU resources.

### Nice-To-Have

- Docker for containerization of the multi-modal conversational agent
- Streamlit for the user interface, hosted on a web server with GPU access (e.g. Hugging Face Spaces)

## Team

- Stephen
- Jutta
- Safak
- Vincenzo

- Bahar Rezaei (DSR alumni)

## Mentors

We have spoken to Dr. Tristan Behrens (NLP) and Krzysztof Buzar (EEG) who are happy to help us with the project!

We've also received enthusiastic support from Dr. Carmen Martínez (Conversational AI at FlixBus), Jacopo Farina (Data Engineer at FlixBus), and Dr. Bob Moore (IBM Watson)!