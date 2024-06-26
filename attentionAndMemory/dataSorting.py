import sqlite3
import numpy as np
import matplotlib.pyplot as plt

def classify_reaction_times(db_path, email, sessionId, testId):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = '''
    SELECT reactionTime
    FROM result
    WHERE email = ? AND sessionId = ? AND testId = ?
    '''
    cursor.execute(query, (email, sessionId, testId))
    data = cursor.fetchall()
    
    conn.close()
    
    if not data:
        print("Aucune donnée trouvée pour l'email fourni.")
        return
    
    reactionTime = np.array([row[0] for row in data])
    
    mean_rt = np.mean(reactionTime)
    std_rt = np.std(reactionTime)
    
    category_below = reactionTime[reactionTime < (mean_rt - std_rt)]
    category_within = reactionTime[(reactionTime >= (mean_rt - std_rt)) & (reactionTime <= (mean_rt + std_rt))]
    category_above = reactionTime[reactionTime > (mean_rt + std_rt)]
    
    print(category_below, category_within, category_above)
    print(len(category_below), len(category_within), len(category_above))
    
    bins = np.linspace(reactionTime.min(), reactionTime.max(), 30)
    plt.figure(figsize=(10, 6))
    plt.hist(category_below, bins=bins, alpha=0.5, label='X < μ - σ', color='red')
    plt.hist(category_within, bins=bins, alpha=0.5, label='μ + σ < X < μ + σ', color='yellow')
    plt.hist(category_above, bins=bins, alpha=0.5, label='> μ + σ', color='green')
    
    plt.xlabel('Temps de réaction (ms)')
    plt.ylabel('Nombre')
    plt.title(f'Tri du temps de réaction de {email} (Session: {sessionId}, Test: {testId})')
    plt.legend()
    plt.grid(True)
    plt.show()

db_path = 'attentionAndMemory/instance/attention.db'
email = 'revillon@example.com'
sessionId = 2
testId = 2

classify_reaction_times(db_path, email, sessionId, testId)