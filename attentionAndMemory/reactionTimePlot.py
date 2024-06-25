import sqlite3
import matplotlib.pyplot as plt

def plot_reaction_time(db_path, email, sessionId, testId):
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
    
    plt.figure(figsize=(10, 6))
    plt.plot(timeCode, reactionTime, marker='o')
    plt.xlabel('Time Code')
    plt.ylabel('Reaction Time')
    plt.title(f'Evolution du temps de réaction de {email} (Session: {sessionId}, Test: {testId})')
    plt.grid(True)
    plt.show()

db_path = 'attentionAndMemory/instance/attention.db'
email = 'strasser@example.com'
sessionId = 1
testId = 2

plot_reaction_time(db_path, email, sessionId, testId)
