import numpy as np
import matplotlib.pyplot as plt
import splitSignal as ss

def classify_reaction_times(dbpath, email, sessionId, testId):
    reactionTimes, timeCodes = ss.getDataForSession(dbpath, email, sessionId, testId)
    filteredReactionTimes = [rt for rt in reactionTimes if rt != 1700]
    sortedTimeCodes = sorted(timeCodes)
    timeCodeRanks = {timeCode: rank for rank, timeCode in enumerate(sortedTimeCodes)}
    
    mu = np.mean(filteredReactionTimes)
    sigma = np.std(filteredReactionTimes)
    print(sigma)
    
    rt_1, rt_2, rt_3 = [], [], []
    tc_1, tc_2, tc_3 = [], [], []
    tco_1, tco_2, tco_3 = [], [], []

    for rt, tc in zip(reactionTimes, timeCodes):
        if rt < mu - sigma:
            rt_1.append(rt)
            tc_1.append(tc)
            tco_1.append(timeCodeRanks[tc])
        elif mu - sigma <= rt <= mu + sigma:
            rt_2.append(rt)
            tc_2.append(tc)
            tco_2.append(timeCodeRanks[tc])
        else:
            rt_3.append(rt)
            tc_3.append(tc)
            tco_3.append(timeCodeRanks[tc])

    print(len(rt_1), len(rt_2), len(rt_3))
    
    #bins = np.linspace(min(reactionTimes), max(reactionTimes), 30)
    #plt.figure(figsize=(10, 6))
    #plt.hist(rt_1, bins=bins, alpha=0.5, label='X < μ - σ', color='green')
    #plt.hist(rt_2, bins=bins, alpha=0.5, label='μ + σ < X < μ + σ', color='yellow')
    #plt.hist(rt_3, bins=bins, alpha=0.5, label='> μ + σ', color='red')
    #
    #plt.xlabel('Temps de réaction (ms)')
    #plt.ylabel('Nombre')
    #plt.title(f'Tri du temps de réaction de {email} (Session: {sessionId}, Test: {testId})')
    #plt.legend()
    #plt.grid(True)
    #plt.show()
    
    return [tco_1, tco_2, tco_3]


def getAllData(db_path):
    emails = ["kayssieh@example.com", "revillon@example.com", "yvert@example.com", "strasser@example.com"]
    names = ["Kayssieh", "Revillon", "Yvert", "Strasser"]
    pairs = [[1,1], [1,2], [2,2], [3,2]]
    for i, email in enumerate(emails):
        for pair in pairs:
            if pair != [3,2] or email != "strasser@example.com":
                sessionId, testId = pair
                results = classify_reaction_times(db_path, email, sessionId, testId)
                with open(f'{names[i]}-session{sessionId}-test{testId}.txt', 'w') as file:
                    for line in results:
                         file.write(f"{line}\n")
                print(f"Results for {names[i]} (Session: {sessionId}, Test: {testId}) saved in {names[i]}-session{sessionId}-test{testId}.txt")


db_path = 'attentionAndMemory/instance/attention.db'
getAllData(db_path)