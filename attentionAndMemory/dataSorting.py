import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import splitSignal as ss

def classify_reaction_times(dbpath, email, sessionId, testId):
    reactionTimes, timeCodes = ss.getDataForSession(dbpath, email, sessionId, testId)
    filtered_reactionTimes = [rt for rt in reactionTimes if rt != 1700]
    
    mu = np.mean(filtered_reactionTimes)
    sigma = np.std(filtered_reactionTimes)
    print(sigma)
    
    rt_1, rt_2, rt_3 = [], [], []
    tc_1, tc_2, tc_3 = [], [], []

    for rt, tc in zip(reactionTimes, timeCodes):
        if rt < mu - sigma:
            rt_1.append(rt)
            tc_1.append(tc)
        elif mu - sigma <= rt <= mu + sigma:
            rt_2.append(rt)
            tc_2.append(tc)
        else:
            rt_3.append(rt)
            tc_3.append(tc)

    print(len(rt_1), len(rt_2), len(rt_3))
    
    bins = np.linspace(min(reactionTimes), max(reactionTimes), 30)
    plt.figure(figsize=(10, 6))
    plt.hist(rt_1, bins=bins, alpha=0.5, label='X < μ - σ', color='green')
    plt.hist(rt_2, bins=bins, alpha=0.5, label='μ + σ < X < μ + σ', color='yellow')
    plt.hist(rt_3, bins=bins, alpha=0.5, label='> μ + σ', color='red')
    
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