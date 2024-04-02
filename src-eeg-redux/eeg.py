import numpy as np
import time
import subprocess
from pylsl import StreamInlet, resolve_byprop
import utils
import shared  # Import the shared module to access the pause_duration variable
import gc
from speaker import generate_speech  # Import the generate_speech function from speaker.py

class Band:
    """Enumeration for EEG frequency bands."""
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

# Experimental parameters
BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = [2]

# Neurofeedback thresholds
ALPHA_RELAXATION_THRESHOLD = 0.5
BETA_ACTIVATION_THRESHOLD = 0.4
THETA_RELAXATION_THRESHOLD = 0.5

def initialize_stream():
    gc.collect()
    subprocess.Popen(["muselsl", "stream"], shell=False)
    print('Looking for an EEG stream...')
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        streams = resolve_byprop('type', 'EEG', timeout=2)
        if streams:
            print('EEG stream found!')
            return StreamInlet(streams[0], max_chunklen=12)
        else:
            attempts += 1
            print(f'No EEG stream found. Attempt {attempts} of {max_attempts}. Retrying...')

        if attempts == max_attempts:
            print("Failed to find EEG stream after 3 attempts.")
            return None

        time.sleep(2)

def compute_metrics(eeg_inlet, fs):
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None
    band_buffer = np.zeros((int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1)), 4))

    alpha_metrics, theta_metrics, beta_metrics = [], [], []
    start_time = time.time()
    end_time = start_time + shared.pause_duration

    try:
        while time.time() < end_time:
            eeg_data, timestamp = eeg_inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
            if not eeg_data:
                continue

            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
            eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)
            data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
            band_powers = utils.compute_band_powers(data_epoch, fs)

            band_buffer, _ = utils.update_buffer(band_buffer, band_powers)

            smooth_band_powers = np.mean(band_buffer, axis=0)
            alpha_metric, beta_metric, theta_metric = compute_individual_metrics(smooth_band_powers)
            alpha_metrics.append(alpha_metric)
            theta_metrics.append(theta_metric)
            beta_metrics.append(beta_metric)

    except KeyboardInterrupt:
        print('Closing!')
    finally:
        mental_state = update_metrics(alpha_metrics, theta_metrics, beta_metrics)
        gc.collect()

    return mental_state

def print_band_powers(smooth_band_powers):
    print('Delta: {:.2f}, Theta: {:.2f}, Alpha: {:.2f}, Beta: {:.2f}'.format(*smooth_band_powers))

def compute_individual_metrics(smooth_band_powers):
    alpha_metric = smooth_band_powers[Band.Alpha] / smooth_band_powers[Band.Delta]
    beta_metric = smooth_band_powers[Band.Beta] / smooth_band_powers[Band.Theta]
    theta_metric = smooth_band_powers[Band.Theta] / smooth_band_powers[Band.Alpha]
    print('Alpha Relaxation: {:.2f}, Beta Concentration: {:.2f}, Theta Relaxation: {:.2f}'.format(alpha_metric, beta_metric, theta_metric))
    return alpha_metric, beta_metric, theta_metric

def update_metrics(alpha_metrics, theta_metrics, beta_metrics):
    mean_alpha = np.mean(alpha_metrics)
    mean_theta = np.mean(theta_metrics)
    mean_beta = np.mean(beta_metrics)
    mental_state = determine_mental_state(mean_alpha, mean_theta, mean_beta)

    print(f"Mental State: {mental_state}")

    try:
        generate_speech(mental_state)  # Use the generate_speech function from speaker.py instead of gTTS
    except Exception as e:
        print(f"Error using generate_speech: {e}")
    finally:
        gc.collect()

    return mental_state

def determine_mental_state(mean_alpha, mean_theta, mean_beta):
    if (mean_alpha + mean_theta) > (ALPHA_RELAXATION_THRESHOLD + THETA_RELAXATION_THRESHOLD):
        return "You're relaxed"
    elif mean_beta > BETA_ACTIVATION_THRESHOLD:
        return "You're active"
    return "Remember Jhana's guidance"
