  
# -*- coding: utf-8 -*-
"""
This is a code to record EEG data from Muse S. This will export five different .csv files as the following
* 1/(Theta/Beta Ratio)
* Alpha Power 
* Beta Power
* Delta Power
* Theta Power

@author: Kern Simon Kim
"""

import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import multiprocessing
import pandas as pd
import keyboard

# Handy little enum to make code more readable


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


""" EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0, 1, 2, 3]

# Data frame for TBR, alpha wave power, beta wave power, theta wave power, and delta wave power
TBR = pd.DataFrame()
alphaP = pd.DataFrame()
betaP = pd.DataFrame()
deltaP = pd.DataFrame()
thetaP = pd.DataFrame()



def shift1Fill(dataBuffer, inputData):
    new_buffer = np.concatenate((dataBuffer, inputData), axis=0)
    new_buffer = new_buffer[1:, :]

    return new_buffer


if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 4))
    filter_state = None  # for use with the notch filter

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta]
    band_buffer = np.zeros((n_win_test, 4, 4))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')
    eventCode = '0'
                
    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True: 
            if keyboard.is_pressed("1"): # Gain focus
                eventCode = 1
            elif keyboard.is_pressed("2"): # Lost focus
                eventCode = 2
            else:                                          
                eventCode = 0                      

            """ 3.1 ACQUIRE DATA """
            # Obtain EEG data from the LSL stream
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))

            # Only keep the channel we're interested in
            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
            # Update EEG buffer with the new data
            eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True,filter_state=filter_state)

            """ 3.2 COMPUTE BAND POWERS """
            # Get newest samples from the buffer
            data_epoch = utils.get_last_data(eeg_buffer,EPOCH_LENGTH * fs)

            # Compute band powers
            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer, np.asarray([band_powers]))
            # Compute the average band powers for all epochs in buffer
            # This helps to smooth out noise
            smooth_band_powers = np.mean(band_buffer, axis=0)

            """ 3.3 COMPUTE NEUROFEEDBACK METRICS """

            TBR_metric = smooth_band_powers[Band.Beta] / \
                    smooth_band_powers[Band.Theta]

            alpha_metric = smooth_band_powers[Band.Alpha]
            beta_metric = smooth_band_powers[Band.Beta]
            theta_metric = smooth_band_powers[Band.Theta]
            delta_metric  = smooth_band_powers[Band.Delta]
            
            dataTBR = [eventCode, TBR_metric[0], TBR_metric[1], TBR_metric[2], TBR_metric[3]]
            dataAlpha = [eventCode, alpha_metric[0], alpha_metric[1], alpha_metric[2], alpha_metric[3]]
            dataBeta = [eventCode, beta_metric[0], beta_metric[1], beta_metric[2], beta_metric[3]]
            dataDelta = [eventCode, delta_metric[0], delta_metric[1], delta_metric[2], delta_metric[3]]
            dataTheta = [eventCode, theta_metric[0], theta_metric[1], theta_metric[2], theta_metric[3]]

            dfTBR = pd.DataFrame([dataTBR], index = [timestamp[0]], columns = ["Event Code", "Left Ear","Left Forehead", "Right Forehead", "Right Ear"])
            dfalpha = pd.DataFrame([dataAlpha], index = [timestamp[0]], columns = ["Event Code", "Left Ear","Left Forehead", "Right Forehead", "Right Ear"])
            dfbeta = pd.DataFrame([dataBeta], index = [timestamp[0]], columns = ["Event Code", "Left Ear","Left Forehead", "Right Forehead", "Right Ear"])
            dfdelta = pd.DataFrame([dataDelta], index = [timestamp[0]], columns = ["Event Code", "Left Ear","Left Forehead", "Right Forehead", "Right Ear"])
            dftheta = pd.DataFrame([dataTheta], index = [timestamp[0]], columns = ["Event Code", "Left Ear","Left Forehead", "Right Forehead", "Right Ear"])
            
            TBR = TBR.append(dfTBR)
            alphaP = alphaP.append(dfalpha)
            betaP = betaP.append(dfbeta)
            deltaP = deltaP.append(dfdelta)
            thetaP = thetaP.append(dftheta)     
    except KeyboardInterrupt:
        print('Closing!')

    TBR.to_csv(r'C:\Users\Kern Simon Kim\Documents\MATLAB\BIOEN461\reading_TBR.csv')
    alphaP.to_csv(r'C:\Users\Kern Simon Kim\Documents\MATLAB\BIOEN461\reading_alpha.csv')
    betaP.to_csv(r'C:\Users\Kern Simon Kim\Documents\MATLAB\BIOEN461\reading_beta.csv')
    deltaP.to_csv(r'C:\Users\Kern Simon Kim\Documents\MATLAB\BIOEN461\reading_delta.csv')
    thetaP.to_csv(r'C:\Users\Kern Simon Kim\Documents\MATLAB\BIOEN461\reading_theta.csv')
