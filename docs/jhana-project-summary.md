# `Jhāna.AI`: Personal Meditation Guide

# Project Summary

`Jhāna.AI` is an interactive voice assistant which uses real-time brain sensing to guide the user in ancient Jhana Meditation, for reaching states of concentration, bliss and calm, and finding relief from pain. `Jhāna.AI` uses cutting-edge technologies of biofeedback, deep learning, and natural speech interaction for personalised guided meditation sessions. :woman_in_lotus_position::robot_face::pray: 

## Overview

Jhāna is a cutting-edge conversational agent providing voice assistance to guide you in meditation. 

In summary, Jhāna provides the following features:

- Multi-modal assistance allowing text or speech interaction with brain-sensing to provide real-time feedback to the user during meditation.

- Trained on a dataset of expert-level guided Jhāna meditations, and uses an EEG brain sensing headband (Muse 2) to monitor the user's meditation state and provide feedback in real-time, augmented with scientific articles and user's meditation history. 

- Provides personalised expert-level guided meditations, answers questions about meditation, and provides feedback on the user's meditation state in real-time.

## Problem Statement

Jhāna addresses the following problems:

- Chronic pain and stress are two of the most common health problems in the world. Meditation is a potential remedy for these problems, but many people find it difficult to get started with meditation. Our age is characterized by a high level of distraction. Even experienced meditators can struggle to maintain a consistent practice.

- Meditation apps are very popular, and growing in popularity, but they are limited in their ability to provide personalised voice-assistance and interactive feedback to the user. They can provide guided meditations, but they cannot provide real-time feedback on the user's meditation state. This makes it difficult for the user to know if the instructions are suitable for their condition, and difficult to sustain attention and focus during meditation.

- The most commonly taught meditations in the West are mindfulness and relaxation meditations. However, there are other types of meditation that have great potential for relieving chronic pain and stress, such as Jhāna meditation. Jhāna meditation is a type of concentration meditation that is designed to produce deep states of bliss and tranquility. But these states are difficult to achieve without guidance, are rarely taught in the West, except by expert teachers in Buddhist and Hindu retreat settings. They are not widely accessible to the general public.

## Our Solution

Jhāna is part of a new generation of meditation apps: a cutting-edge conversational agent that provides voice assistance to guide you in a personalised meditation.

- Jhāna AI helps the user achieve jhāna states by providing guided meditations, answering questions about meditation, and giving feedback on your meditation progress. 

- Ask Jhāna with text or speech to guide you through a meditation, and it will provide real-time feedback on your meditation state, and help you to achieve deep states of meditation.

- Jhāna is trained on expert-level meditation instructions, and can provide you with personalised guidance, by retrieving and generating responses from a curated dataset of guided Jhāna meditations.

- Jhāna monitors your meditation state using an EEG brain sensing headband (Muse 2), consults your meditation history and relevant scientific articles, and provides real-time feedback as you meditate.

- Jhāna is designed to be accessible to everyone, including those with chronic pain and stress, and those who are new to meditation. It is designed to be easy to use, and to provide expert-level guidance from teachers not available to most people, who will help you achieve deep states of meditation.

The next generation of meditation apps like Jhāna will be multi-modal conversational agents, offering voice interaction and provide real-time feedback to you during meditation, which are powered by Artificial Intelligence. In the future, Jhāna could be available within a Virtual Reality environment, making ancient meditation teachings available for all.

## Tech Stack

Jhāna is an interactive voice assistant built with the following technologies, which are mostly open source and state-of-the-art:

### Baseline

- **Automated Speech Recognition (ASR)** for converting user speech to text (OpenAI Whisper)
- **Large Language Model (LLM)** trained on a curated dataset of guided jhāna meditations, for understanding user intent and generating responses. Hosted locally using fine-tuning of pre-trained models with `ollama` (e.g. Microsoft Phi 2, llama2, Mistral, Mixtral, stablelm2) or cloud-based with OpenAI Agents (e.g. GPT-3.5, GPT-4).
- **EEG brain sensing headband (Muse 2)** for monitoring user's meditation state.
- `LangChain` for managing the multi-modal conversational agent and providing Retrieval Augmented Generation (RAG) for generating responses from database and web sources of texts (e.g. medical texts, meditation texts, scientific articles).
- **Text-To-Speech (TTS)** for converting the assistant's responses to speech with voice cloning (Coqui `XTTS-v2`)
- `Docker` for containerization of development environment, to allow for collaboration and deployment, including sharing GPU resources via API (backup plan: `Colab Pro`).

### Deployment

Our aim is to deploy Jhāna on a web server with GPU access for easy access via a web browser with text or speech interaction.

- `Docker` will be used to containerise the Jhāna app, to allow for deployment and sharing of the conversational agent with the user.

- `Streamlit` for the user interface, hosted on a web server with GPU access (e.g. AWS, Hugging Face Spaces, Heroku).

## Collaborators

- [Bahar](https://github.com/Bahar-Rezaei)
- [Jutta](https://github.com/juttaromberg)
- [Safak](https://github.com/ozdensafak)
- [Vincenzo](https://github.com/Vinsora)

## Mentors

Dr. Tristan Behrens (NLP) and Krzysztof Buzar (EEG) are the project mentors at Data Science Retreat.

We gratefully appreciate expert guidance from Dr. Carmen Martínez (Conversational AI at FlixBus), Jacopo Farina (Data Engineer at FlixBus), and Dr. Bob Moore (IBM Watson).