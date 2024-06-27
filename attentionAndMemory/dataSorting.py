import numpy as np
import matplotlib.pyplot as plt
import splitSignal as ss
import signalTreatment as st

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

    #print(len(rt_1), len(rt_2), len(rt_3))
    
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


def classify_reaction_times_module(reactionTimes, timeCodes, nb_splits=3):
    # if email == "chandiramani@example.com":
    #     reactionTimes, timeCodes = ss.getDataForPrishaSession(dbpath, email, sessionId, testId)
    # else:
    #     reactionTimes, timeCodes = ss.getDataForSession(dbpath, email, sessionId, testId)

    filteredReactionTimes = [rt for rt in reactionTimes if rt != 1700]
    
    mu = np.mean(filteredReactionTimes)
    sigma = np.std(filteredReactionTimes)
    # print(sigma)
    
    result = []
    if nb_splits == 3:
        for rt, tc in zip(reactionTimes, timeCodes):
            if rt < mu - sigma:
                result.append([0, 0, 1])
            elif mu - sigma <= rt <= mu + sigma:
                result.append([0, 1, 0])
            else:
                result.append([1, 0, 0])
    if nb_splits == 5:
        for rt, tc in zip(reactionTimes, timeCodes):
            if rt <= mu - sigma:
                result.append([0, 0, 0, 0, 1])
            elif mu - sigma < rt <= mu - sigma/2:
                result.append([0, 0, 0, 1, 0])
            elif mu - sigma/2 < rt < mu + sigma/2:
                result.append([0, 0, 1, 0, 0])
            elif mu + sigma/2 < rt <= mu + sigma:
                result.append([0, 1, 0, 0, 0])
            elif mu + sigma:
                result.append([1, 0, 0, 0, 0])

    return np.array(result)

def parseFileName(fileName):
    s = fileName.split('_')
    name, _, gameType, sessionId = s[0], s[1], s[2], s[3]
    filenames_emails = {"Kayssieh":"kayssieh@example.com", "Revillon":"revillon@example.com", "Yvert":"yvert@example.com", "Strasser":"strasser@example.com", "Chandiramani":"chandiramani@example.com"}
    email = filenames_emails[name]
    if gameType == "Congruent":
        testId = 1
    else:
        testId = 2
    sessionId = int(sessionId.split('.')[0]) 

    return name, email, sessionId, testId

def get_files_in_folder(folder_path):
        import os
        files = []
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                files.append(file)
        return files

def filePathFromFileName(fileName):
    name, email, sessionId, testId = parseFileName(fileName)
    if name == "Chandiramani":
        file_path = 'C:/Users/quent/Télécom/Cours/Proj/Proj104/aiot/attentionAndMemory/signaux EEG Prisha/' + fileName
    else: 
        file_path = 'C:/Users/quent/Télécom/Cours/Proj/Proj104/aiot/attentionAndMemory/signaux EEG/' + fileName
    return file_path

def reactionTimesAndTimeCodesFromFileName(fileName):
    name, email, sessionId, testId = parseFileName(fileName)
    if name == "Chandiramani":
        dbpath = 'C:/Users/quent/Télécom/Cours/Proj/Proj104/aiot/attentionAndMemory/instance Prisha/attention.db'
        reactionTimes, timeCodes = ss.getDataForPrishaSession(dbpath, email, sessionId, testId)
    else:
        dbpath = 'C:/Users/quent/Télécom/Cours/Proj/Proj104/aiot/attentionAndMemory/instance/attention.db'
        reactionTimes, timeCodes = ss.getDataForSession(dbpath, email, sessionId, testId)
    return reactionTimes, timeCodes
        

def getDataAndLabels(fileName):
    filePath = filePathFromFileName(fileName)
    reactionTimes, timeCodes = reactionTimesAndTimeCodesFromFileName(fileName)
    

    labels = classify_reaction_times_module(reactionTimes, timeCodes, nb_splits=3)
    data = st.fftChunksFromFile(filePath, timeCodes)
    
    return data, labels

    
if __name__ == "__main__":
    # x, y = getDataAndLabels("Kayssieh_Charles_NonCongruent_2.xdf")
    # print(len(x), len(y))
    x, y = getDataAndLabels("Revillon_Quentin_NonCongruent_1.xdf")
    print(len(x), len(y))
