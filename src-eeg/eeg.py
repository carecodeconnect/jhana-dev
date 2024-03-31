import numpy as np
import time
import subprocess
from pylsl import StreamInlet, resolve_byprop
import utils
from gtts import gTTS
from playsound import playsound
import shared  # Import the shared module to access the pause_duration variable
import gc

class Band:
    """Enumeration for EEG frequency bands."""
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

# Experimental parameters (modifiable to change aspects of the signal processing)
BUFFER_LENGTH = 5  # Length of the EEG data buffer in seconds
EPOCH_LENGTH = 1  # Length of the epochs used to compute the FFT in seconds
OVERLAP_LENGTH = 0.8  # Amount of overlap between two consecutive epochs in seconds
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH  # Shift for the start of each epoch
INDEX_CHANNEL = [2]  # Index of the channel(s) to be used

# Neurofeedback thresholds
ALPHA_RELAXATION_THRESHOLD = 0.5
BETA_ACTIVATION_THRESHOLD = 0.4
THETA_RELAXATION_THRESHOLD = 0.5

def initialize_stream():
    """Initialize and return the EEG stream inlet, trying up to 3 times."""
    gc.collect()  # Optional, if experiencing memory issues
    subprocess.Popen(["muselsl", "stream"], shell=False)  # Start the stream in a subprocess
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
            return None  # or handle as appropriate for your application

        time.sleep(2)  # Wait for 2 seconds before trying again

# def compute_metrics(eeg_inlet, fs):
#     """Compute and print neurofeedback metrics from EEG data, dynamically using the shared pause duration."""
#     eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
#     filter_state = None
#     band_buffer = np.zeros((int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1)), 4))

#     alpha_metrics, theta_metrics, beta_metrics = [], [], []
#     start_time = time.time()
#     end_time = start_time + shared.pause_duration  # Determine the end time based on pause_duration

#     try:
#         while time.time() < end_time:  # Run until the current time is less than the end time
#             eeg_data, timestamp = eeg_inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
#             if not eeg_data:
#                 continue  # If no data, skip to the next iteration

#             ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
#             eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)
#             data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
#             band_powers = utils.compute_band_powers(data_epoch, fs)

#             print("band_powers dimensions:", band_powers.shape)
#             band_buffer, _ = utils.update_buffer(band_buffer, band_powers)

#             smooth_band_powers = np.mean(band_buffer, axis=0)
#             print_band_powers(smooth_band_powers)

#             alpha_metric, beta_metric, theta_metric = compute_individual_metrics(smooth_band_powers)
#             alpha_metrics, theta_metrics, beta_metrics = update_metrics(alpha_metrics, theta_metrics, beta_metrics, alpha_metric, beta_metric, theta_metric)  # Adjusted call

#     except KeyboardInterrupt:
#         print('Closing!')
#     finally:
#         gc.collect()  # Clean up after session

def compute_metrics(eeg_inlet, fs):
    """Compute and print neurofeedback metrics from EEG data, and determine the mental state just before the pause duration ends."""
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None
    band_buffer = np.zeros((int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1)), 4))

    alpha_metrics, theta_metrics, beta_metrics = [], [], []
    start_time = time.time()
    end_time = start_time + shared.pause_duration  # Determine the end time based on pause_duration

    try:
        while time.time() < end_time:  # Run until the current time is less than the end time
            eeg_data, timestamp = eeg_inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
            if not eeg_data:
                continue  # If no data, skip to the next iteration

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
        # Calculate and announce the mental state just before exiting
        mental_state = update_metrics(alpha_metrics, theta_metrics, beta_metrics)
        gc.collect()  # Clean up after session

    return mental_state

def print_band_powers(smooth_band_powers):
    """Print the computed band powers."""
    print('Delta: {:.2f}, Theta: {:.2f}, Alpha: {:.2f}, Beta: {:.2f}'.format(*smooth_band_powers))

def compute_individual_metrics(smooth_band_powers):
    """Compute and return individual neurofeedback metrics."""
    alpha_metric = smooth_band_powers[Band.Alpha] / smooth_band_powers[Band.Delta]
    beta_metric = smooth_band_powers[Band.Beta] / smooth_band_powers[Band.Theta]
    theta_metric = smooth_band_powers[Band.Theta] / smooth_band_powers[Band.Alpha]
    print('Alpha Relaxation: {:.2f}, Beta Concentration: {:.2f}, Theta Relaxation: {:.2f}'.format(alpha_metric, beta_metric, theta_metric))
    return alpha_metric, beta_metric, theta_metric

# def update_metrics(alpha_metrics, theta_metrics, beta_metrics, alpha_metric, beta_metric, theta_metric):
#     """Update and evaluate metrics to determine the mental state."""
#     alpha_metrics.append(alpha_metric)
#     theta_metrics.append(theta_metric)
#     beta_metrics.append(beta_metric)

#     # Calculate the mean metrics to determine the mental state
#     mean_alpha = np.mean(alpha_metrics)
#     mean_theta = np.mean(theta_metrics)
#     mean_beta = np.mean(beta_metrics)
#     mental_state = determine_mental_state(mean_alpha, mean_theta, mean_beta)

#     print(f"Mental State: {mental_state}")

#     try:
#         tts = gTTS(text=mental_state, lang='en')
#         tts.save("mental_state.mp3")
#         playsound("mental_state.mp3")
#     except Exception as e:
#         print(f"Error using gTTS: {e}")
#     finally:
#         gc.collect()

#     # Optionally, you might reset the metrics after evaluating the mental state
#     # This depends on whether you want to accumulate metrics across pauses or evaluate each pause independently
#     # alpha_metrics, theta_metrics, beta_metrics = [], [], []

#     # Return the updated metrics lists
#     return alpha_metrics, theta_metrics, beta_metrics

def update_metrics(alpha_metrics, theta_metrics, beta_metrics):
    """Update and evaluate metrics to determine the mental state."""
    # Calculate the mean metrics to determine the mental state
    mean_alpha = np.mean(alpha_metrics)
    mean_theta = np.mean(theta_metrics)
    mean_beta = np.mean(beta_metrics)
    mental_state = determine_mental_state(mean_alpha, mean_theta, mean_beta)

    print(f"Mental State: {mental_state}")

    try:
        tts = gTTS(text=mental_state, lang='en')
        tts.save("mental_state.mp3")
        playsound("mental_state.mp3")
    except Exception as e:
        print(f"Error using gTTS: {e}")
    finally:
        gc.collect()

    return mental_state

def determine_mental_state(mean_alpha, mean_theta, mean_beta):
    """Determine and return the mental state based on the computed metrics."""
    if (mean_alpha + mean_theta) > (ALPHA_RELAXATION_THRESHOLD + THETA_RELAXATION_THRESHOLD):
        return "You're relaxed"
    elif mean_beta > BETA_ACTIVATION_THRESHOLD:
        return "You're active"
    return "Remember Jhana's guidance"
