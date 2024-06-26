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

def padchunks(chunks):
    padded_chunks = []
    for chunk in chunks:
        if chunk.shape[0] < int(5600/4):
            chunk = np.pad(chunk, ((0, 1400-chunk.shape[0]), (0, 0)), 'constant')
        
        padded_chunks.append(chunk)
    return padded_chunks

if __name__ == "__main__":
    print()

    data = ss.getAllData("./instance/attention.db")
    # file_name = "Revillon_Quentin_NonCongruent_1.xdf"
    file_names = ss.get_files_in_folder('./signaux EEG')
 
    for file_name in file_names[:]:
        eegchunks, timechunks = fileTochunks(file_name, data)
        print(eegchunks[0].shape, timechunks[0].shape)


        pad = padchunks(eegchunks)
        # print(pad[0])
        print(pad[0].shape)
        # print(pad[0])
        # print(timechunks[0])
        # maxi = getMaxTimechunk(timechunks)
        # print(maxi)

    # print(eegchunks[0].shape, timechunks[0].shape)
    
    
