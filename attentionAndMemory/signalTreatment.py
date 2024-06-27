import os
import numpy as np
import pyxdf
import splitSignal as ss

def read_xdf_file(filepath):
    # Lire le fichier XDF
    streams, header = pyxdf.load_xdf(filepath)
    # Trouver le flux EEG (souvent il a un 'type' ou 'name' spécifique, ajustez si nécessaire)
    eeg_stream = next((stream for stream in streams if stream['info']['name'][0] == 'EEG'), None)
    if not eeg_stream:
        raise ValueError("No EEG stream found in the XDF file")
    
    # Récupérer les données EEG
    eeg_data = eeg_stream['time_series']
    # Récupérer les timestamps
    timestamps = eeg_stream['time_stamps']
    return eeg_data, timestamps

def inspect_xdf_metadata(filepath):
    streams, header = pyxdf.load_xdf(filepath)
    
    for stream in streams:
        print(f"Stream Name: {stream['info']['name'][0]}")
        print(f"Stream Type: {stream['info']['type'][0]}")
        print(f"Sample Rate: {stream['info']['nominal_srate'][0]}")
        print("Metadata:")
        for key, value in stream['info'].items():
            if key != 'name' and key != 'type':
                print(f"  {key}: {value}")
        print("\n")


def makechunks(eeg_data, timeStamps, timeCodes):
    """cette fonction découpe les données EEG en chunks en fonction des timeCodes, à un intervalle de timeCodes est associé un chunk"""
    timeStamps = (np.array(timeStamps) - timeStamps[0])*1000
    # timechunks = np.array([])
    # eegchunks = np.array([])
    timechunks = []
    eegchunks = []
    previousIStamps = 0
    iStamps = 0
    # print(timeStamps[-1])
    # print(timeCodes[-1])
    for timeCode in timeCodes:
        while timeStamps[iStamps] < timeCode:
            iStamps += 1
        eegchunks.append(eeg_data[previousIStamps:iStamps])
        timechunks.append(timeStamps[previousIStamps:iStamps])
        # np.vstack((eegchunks, eeg_data[previousIStamps:iStamps]))
        # np.vstack((timechunks, timeStamps[previousIStamps:iStamps]))
        previousIStamps = iStamps
    return eegchunks, timechunks

def getMaxTimechunk(timechunks):
    # print(eegchunks[0].shape, timechunks[0].shape)
    maxi = 0
    for i in range(len(timechunks)):
        # print(eegchunks[i].shape, timechunks[i].shape)
        if timechunks[i].shape[0] > maxi:
            maxi = timechunks[i].shape[0]
            
    return maxi

def fileTochunks(fileName, data):
    eeg_data, timestamps = read_xdf_file("./signaux EEG/"+fileName)
    reactionTimes, timeCodes = data[fileName]
    eegchunks, timechunks = makechunks(eeg_data, timestamps, timeCodes)
    return eegchunks, timechunks

def padchunks(chunks, pad_size=1400):
    padded_chunks = []
    for chunk in chunks:
        
        if chunk.shape[0] < int(pad_size):
            chunk = np.pad(chunk, ((0, pad_size-chunk.shape[0]), (0, 0)), 'constant')
       
        
        padded_chunks.append(chunk)
    return np.array(padded_chunks)

def perform_fft(chunk):
    fs = 256
    fmax = 18
    fmin = 0.5
    nb_freq = 36
    fft_chunk = []
    
    
    for i_elec in range(chunk.shape[1]):
        
        chunk = chunk[:, i_elec]
        fft_elec = np.fft.fft(chunk, n=1536)
        
        if i_elec == 0:
            fft_chunk = np.array(fft_elec)
        else:
            fft_chunk = np.vstack((fft_chunk, fft_elec))

def number_fft(window_size):
    power = 0
    window_tmp = window_size - 1
    while(window_tmp != 1):
        power = power + 1
        window_tmp = int(window_tmp / 2)
    return pow(2,power +1)

def perform_ffts(chunks):
    fs = 256
    f_max_tf = int(256/2)
    fmax = 18
    fmin = 0.5
    nb_freq = 36
    fft_chunk = []

    def square(x): return (np.abs(x))**2
    def decibels(x): return 10*np.log10(x)
    
    nfft = number_fft(1400)

    fft_chunks = np.fft.rfft(chunks, n=nfft, axis=1)
    fft_chunks = fft_chunks[:,:-1,:]
    #nfft/2 est la plage de fréquence, (/2) car on fait rfft, et on découpe en intervalles de 0.5Hz car on fait 256 segments dans un signal qui contient au plus 128Hz
    fft_chunks = fft_chunks.reshape(fft_chunks.shape[0], f_max_tf * 2, int((nfft/2)/fs), fft_chunks.shape[2])

    #we only keep frequencies between 0.5 and 18 Hz
    fft_chunks = fft_chunks[:,:36,:,:]
    fft_chunks = fft_chunks.mean(axis=2)
    fft_chunks = np.apply_along_axis(square, axis=1, arr=fft_chunks)
    fft_chunks = np.apply_along_axis(decibels, axis=1, arr=fft_chunks)

    # fft_chunks = np.apply_along_axis(square, 2, fft_chunks)
    # fft_chunks = np.apply_along_axis(decibels, 2, fft_chunks)

    return fft_chunks

    # for i_elec in range(chunk.shape[1]):
        
    #     # chunk = chunk[:, i_elec]
    #     # fft_elec = np.fft.fft(chunk, n=1536)
        
    #     if i_elec == 0:
    #         fft_chunk = np.array(fft_elec)
    #     else:
    #         fft_chunk = np.vstack((fft_chunk, fft_elec))


    # fft_chunks.append(fft_chunk)
    # return np.array(fft_chunks)
def fftChunksFromFile(file_path, timeCodes):
    eeg_data, timestamps = read_xdf_file(file_path)
    eegchunks, timechunks = makechunks(eeg_data, timestamps, timeCodes)
    pad = padchunks(eegchunks, 2000)
    fft_chunks = perform_ffts(pad)
    return fft_chunks

if __name__ == "__main__":
    0

    # # print(number_fft(1400))
    # # exit()
    # data = ss.getAllData("./instance/attention.db")
    # # file_name = "Revillon_Quentin_NonCongruent_1.xdf"
    # file_names = ss.get_files_in_folder('./signaux EEG')
 
    # for file_name in file_names[:]:
    #     eegchunks, timechunks = fileTochunks(file_name, data)
    #     # print(eegchunks[0].shape, timechunks[0].shape)


    #     pad = padchunks(eegchunks)
    #     # print(pad[0])
    #     # print(pad.shape)
    #     fft_chunks = perform_ffts(pad)
    #     print(fft_chunks.shape)
    #     input()

        
        # print(pad[0])
        # print(timechunks[0])
        # maxi = getMaxTimechunk(timechunks)
        # print(maxi)

    # print(eegchunks[0].shape, timechunks[0].shape)
    
    
