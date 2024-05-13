import pandas as pd
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split
from tensorflow.keras import models, layers
import tensorflow as tf


#SAMPLE RATE IS THE DEFAULT SR(22050)
#transform all audio files into spectrograms using mel-spectrogram and store them in "birds_spec"
repo_path = os.getcwd()
all_spec_path = os.path.join(repo_path,"birds_spec")

#dir that contains folders that contain specs for each bird
if not os.path.exists(all_spec_path):
    os.makedirs(all_spec_path)

all_birds_directory = os.fsencode(os.path.join(repo_path,"birds_audio"))
for bird in os.listdir(all_birds_directory):
    bird_path = os.path.join(all_spec_path, str(bird))

    #dir for specs per bird
    if not os.path.exists(bird_path):
        os.makedirs(bird_path)
    bird_dir = os.fsencode(os.path.join(all_birds_directory, bird))
    for audio in os.listdir(bird_dir):
        audio_name = os.fsdecode(audio)
        if audio_name.endswith(".json"):
            continue
        #default sampling rate(sr) is 22050
        #signal returns an array of frequencies
        signal, sr = librosa.load(os.path.join(bird_dir,audio),duration=5)

        #write the specs data for each audio file into a csv file
        spec_path = os.path.join(bird_path,f"{str(audio_name)} + .csv") 
        if not os.path.exists(spec_path):
            with open(spec_path,'w') as spec_file:
                np.savetxt(spec_path, signal, delimiter=',')


        




#TO PLOT THE SPECTROGRAMS
"""
        # Plot mel-spectrogram
        N_FFT = 1024         
        HOP_SIZE = 1024       
        N_MELS = 128            
        WIN_SIZE = 1024      
        WINDOW_TYPE = 'hann' 
        FEATURE = 'mel'      
        FMIN = 1400 

        S = librosa.feature.melspectrogram(y=signal,sr=sr,
                                            n_fft=N_FFT,
                                            hop_length=HOP_SIZE, 
                                            n_mels=N_MELS, 
                                            htk=True, 
                                            fmin=FMIN, 
                                            fmax=sr/2) 
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S**2,ref=np.max), fmin=FMIN,y_axis='linear')
        plt.colorbar(format='%+2.0f dB')
        plt.show()

"""





