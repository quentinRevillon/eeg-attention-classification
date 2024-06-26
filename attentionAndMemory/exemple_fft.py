import os
import mne
import numpy as np

# 定义根目录路径
root_path = '/data/tuh_eeg/v2.0.1/edf'
threshold = 18000

extrem_path = '/data/extrem_long/extrem.txt'
save_dir = '/datatwo/preprocessed_feature'

def preprocess_eeg(eeg_data, sfreq, patch_length, stride):
    """
    Preprocess EEG data by applying FFT, normalizing, and extracting sliding window patches.
    
    Args:
        eeg_data: Numpy array of EEG data.
        sfreq: Sampling frequency of the EEG data.
        patch_length: The length of each patch after splitting.
        stride: The stride with which to apply the sliding window for patch extraction.
        
    Returns:
        A numpy array of preprocessed data.
    """
    print('start preprocessing.')
    # Apply FFT
    fft_data = np.abs(np.fft.fft(eeg_data, axis=1))
    # Normalize the FFT data by channel
    normalized_data = (fft_data - np.mean(fft_data, axis=1, keepdims=True)) / np.std(fft_data, axis=1, keepdims=True)
    
    patches = []
    # Extract sliding window patches for each channel
    for channel in normalized_data:
        all_patches = np.lib.stride_tricks.sliding_window_view(channel, window_shape=(patch_length,))
        stride_indices = np.arange(0, all_patches.shape[0], stride)
        patches.append(all_patches[stride_indices])
    preprocessed_data = np.concatenate(patches, axis=0)
    return preprocessed_data

def save_chunks(preprocessed_data, chunk_size, save_dir, file_prefix):
    """
    Saves the preprocessed data in chunks to the specified directory.
    
    Args:
        preprocessed_data: The data to be saved.
        chunk_size: The size of each chunk.
        save_dir: Directory where chunks will be saved.
        file_prefix: Prefix for the chunk filenames.
    """
    num_chunks = int(np.ceil(preprocessed_data.shape[0] / chunk_size))
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        chunk = preprocessed_data[start_idx:end_idx]
        
        # Pad the last chunk if it's smaller than the chunk size
        if chunk.shape[0] < chunk_size:
            chunk = np.pad(chunk, ((0, chunk_size - chunk.shape[0]), (0, 0)), 'constant')
        
        # Save each chunk to a file
        chunk_filepath = os.path.join(save_dir, f"{file_prefix}_chunk_{i}.npy")
        np.save(chunk_filepath, chunk)

def process_edf_files(directory, patch_length=128, stride=64, chunk_size=1024, save_dir=save_dir):
    for subdir, dirs, files in os.walk(directory, topdown=True):
        for filename in files:
            if filename.endswith(".edf"):
                filepath = os.path.join(subdir, filename)
                
                try:
                    raw = mne.io.read_raw_edf(filepath, preload=True)
                    print(f"Successfully opened: {filepath}")
                    eeg_data = raw.get_data()  
                    n_samples = len(raw.times)                    
                    sampling_rate = raw.info['sfreq']
                    
                    duration = n_samples / sampling_rate
                    if duration > threshold:
                            
                        with open(extrem_path, 'a') as file:
                            
                            file.write(filepath + '\n')
                    else:
                        # Preprocess the data
                        preprocessed = preprocess_eeg(eeg_data, raw.info['sfreq'], patch_length, stride)
                        save_chunks(preprocessed, chunk_size, save_dir, filename.split('.')[0])
                    
                    raw.close()
                except Exception as e:
                    print(f"Failed to open {filepath}: {e}")


def process_subfolders(root_dir, start_subfolder, max_subfolder):
    for subfolder in range(start_subfolder,max_subfolder + 1):  
        subfolder_path = os.path.join(root_dir, str(subfolder).zfill(3))
        
        with open(extrem_path, 'a') as file:
         
            file.write(subfolder_path + '\n')
        process_edf_files(subfolder_path)



process_subfolders(root_path, 144, 150)