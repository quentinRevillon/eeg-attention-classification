import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_reaction_time_moving_average(db_path, email, sessionId, testId, window_size=5):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = '''
    SELECT reactionTime, timeCode, isCorrect
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
    isCorrect = [row[2] for row in data]
    
    time_dict = defaultdict(list)
    error_dict = defaultdict(list)
    for t, r, c in zip(timeCode, reactionTime, isCorrect):
        time_dict[t].append(r)
        print(time_dict[t])
        error_dict[t].append(1 - c)  # 1 - c to get the error (1 if incorrect, 0 if correct)
    
    unique_timeCode = np.array(list(time_dict.keys()))
    avg_reactionTime = np.array([np.mean(time_dict[t]) for t in unique_timeCode])
    avg_errorRate = np.array([np.mean(error_dict[t]) for t in unique_timeCode])
    
    sorted_indices = np.argsort(unique_timeCode)
    unique_timeCode = unique_timeCode[sorted_indices]
    avg_reactionTime = avg_reactionTime[sorted_indices]
    avg_errorRate = avg_errorRate[sorted_indices]
    
    def moving_average(data, window_size):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    
    smoothed_reactionTime = moving_average(avg_reactionTime, window_size)
    smoothed_errorRate = moving_average(avg_errorRate, window_size)
    smoothed_timeCode = unique_timeCode[:len(smoothed_reactionTime)]
        
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Time Code')
    ax1.set_ylabel('Temps de réaction (ms)', color=color)
    ax1.plot(unique_timeCode, avg_reactionTime, 'o', color=color, label='Données originales')
    ax1.plot(smoothed_timeCode, smoothed_reactionTime, color=color, label='Moyenne Glissante')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    
    ax2.set_ylim([-0.1, 0.9])

    color = 'tab:red'
    ax2.set_ylabel('Taux d\'Erreur', color=color)
    ax2.plot(smoothed_timeCode, smoothed_errorRate, color=color, label='Taux d\'Erreur Normalisé')
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.title(f'Evolution du temps de réaction et taux d\'erreur de {email} (Session: {sessionId}, Test: {testId})')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    db_path = "C:/Users/quent/Télécom/Cours/Proj/Proj104/aiot/attentionAndMemory/instance/attention.db"
    email = 'strasser@example.com'
    sessionId = 1
    testId = 1

    plot_reaction_time_moving_average(db_path, email, sessionId, testId, window_size=10)  # Increase window_size for more smoothing


