
import os
import numpy as np
import DataTrainingUtils as trainData
import AudioUtils as aud
import NeuralNetworkUtils as nn

#SET VARIABLES AND CLASSES
#mainRoot = os.path.normpath(r'C:\Users\JORIGGI00\Documents\MyDOCs\Corpus_lav2')
mainRoot = os.path.normpath('D:\DATA\POLIMI\----TESI-----\Corpus_test')
dirlist = [ item for item in os.listdir(mainRoot) if os.path.isdir(os.path.join(mainRoot, item)) ]
TInArray = []
TOutArray = []

#CREATE TRAINING OUTPUT DATA FILE
#trainData.setDataCorpus()

#MAIN ROUTINE: load one after the other all the audio files for each session
for session in dirlist:
    currentSessionPathText = os.path.join(mainRoot, session)
    currentSessionPathText += '\Sentences_audio'
    directoryAudio = os.path.normpath(currentSessionPathText)
    #print(directoryAudio)
    for dirs, subdir, files in os.walk(directoryAudio):
        #print('Directory: ',dirs)
        for Afile in files:
            #print('Current File: ',Afile)
            audioFilePath = os.path.join(currentSessionPathText, Afile) 
            
            #READ AUDIO FILE: tranform it in a redable array in spectrum
            arrayAudio, sampleRate = aud.getArrayFromAudio(audioFilePath)
            allFrameFFT = aud.getFreqArray(arrayAudio, sampleRate)
            '''allFrame = aud.getFrameArray(arrayAudio, sampleRate) 
            allFrameFFT = aud.getSpectrumFrameArray(allFrame)'''
            
            #READ TRAINING OUTPUT DATA: corresponding to that audio file
            y_code, output, emo, val, text = trainData.getOutputDataFromAudio(Afile.split('.')[0])
            #print('---Coresponding output for Audio ', Afile)
            #print('Name: ',output.split(';')[0],'\nEmotion: ',emo,'\nValence: ',val,'\nTranscription: ',text,'Emo Label code: ', y_code, '\n')
            
            #BUILD THE INPUT TRAINING ARRAY: dim = (#audiofile, #ofFftPerformed, fftWindowSize)
            TInArray.append(allFrameFFT)
            
            #BUILD THE OUTPUT TRAINING ARRAY: dim = (#audiofile, outlabelArray)
            TOutArray.append(y_code)
            
            '''print('\n')
            print('TInArray number of audio file: ', len(TInArray))
            print('TInArray number of timestep (number of FFT window): ', len(TInArray[0]))
            print('TInArray number of freq considered (value is the amplitude in db for each one): ', len(TInArray[0][0]))
            print('TOutArray number of audio file: ', len(TOutArray))
            print('TOutArray number of output label for each file: ', len(TOutArray[0]))
            print('\n')'''
            
            #FEED THE NN: done for 1 session at time, because the groupped audio file array contains only one session files
            nn.RNNModel(np.asarray(TInArray), TOutArray)
            
            #RESET ARRAY: se non viene fatto accumulo in tin e tout tutti i file audio (risultato finale voluto, eseguendo la RNN all'uscita di tutto il ciclo)
            TInArray = []    
            TOutArray = []
            



