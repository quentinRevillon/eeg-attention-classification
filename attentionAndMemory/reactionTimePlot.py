import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_reaction_time_moving_average(db_path, email, sessionId, testId, window_size=5):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = '''
    SELECT reactionTime, timeCode
    FROM result
    WHERE email = ? AND sessionId = ? AND testId = ?
    ORDER BY timeCode
    '''
    cursor.execute(query, (email, sessionId, testId))
    data = cursor.fetchall()
    
    conn.close()
    
    if not data:
        print("Aucune donnée trouvée pour les paramètres fournis.")
        return
    
    reactionTime = [row[0] for row in data]
    timeCode = [row[1] for row in data]
    
    time_dict = defaultdict(list)
    for t, r in zip(timeCode, reactionTime):
        time_dict[t].append(r)
    
    unique_timeCode = np.array(list(time_dict.keys()))
    avg_reactionTime = np.array([np.mean(time_dict[t]) for t in unique_timeCode])
    
    sorted_indices = np.argsort(unique_timeCode)
    unique_timeCode = unique_timeCode[sorted_indices]
    avg_reactionTime = avg_reactionTime[sorted_indices]
    
    def moving_average(data, window_size):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    
    smoothed_reactionTime = moving_average(avg_reactionTime, window_size)
    smoothed_timeCode = unique_timeCode[:len(smoothed_reactionTime)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(unique_timeCode, avg_reactionTime, 'o', label='Données originales')
    
    plt.plot(smoothed_timeCode, smoothed_reactionTime, label='Moyenne Glissante')
    
    plt.xlabel('Time Code')
    plt.ylabel('Temps de réaction (ms)')
    plt.title(f'Evolution du temps de réaction de {email} (Session: {sessionId}, Test: {testId})')
    plt.legend()
    plt.grid(True)
    plt.show()

db_path = 'attentionAndMemory/instance/attention.db'
email = 'revillon@example.com'
sessionId = 1
testId = 2

plot_reaction_time_moving_average(db_path, email, sessionId, testId, window_size=10)  # Increase window_size for more smoothing
