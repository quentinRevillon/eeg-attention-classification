import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_reaction_time_distribution(db_path, email, sessionId, testId):
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
        print("Aucune donnée trouvée pour les paramètres fournis.")
        return
    
    reaction_times = [row[0] for row in data]
    
    plt.figure(figsize=(10, 6))
    sns.histplot(reaction_times, kde=True, bins=30)
    plt.xlabel('Reaction Time')
    plt.ylabel('Count')
    plt.title(f'Distribution du temps de réaction de {email} (Session: {sessionId}, Test: {testId})')
    plt.grid(True)
    plt.show()

db_path = 'attentionAndMemory/instance/attention.db'
email = 'strasser@example.com'
sessionId = 1
testId = 2

plot_reaction_time_distribution(db_path, email, sessionId, testId)
