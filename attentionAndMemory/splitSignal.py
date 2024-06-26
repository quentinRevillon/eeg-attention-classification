import sqlite3
import os
import matplotlib.pyplot as plt

def getReactionTimesAndTimeCodesAndIsCorrect(db_path, email, sessionId, testId):
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
    
    reactionTime = [data[i][0] for i in range(len(data))]
    timeCode = [data[i][1] for i in range(len(data))]
    isCorrect = [data[i][2] for i in range(len(data))]
    
    return reactionTime, timeCode, isCorrect


def isNotCorrectTo1700(reactionTimes, timeCodes, isCorrect):

    for i in range(len(isCorrect)):
        if isCorrect[i] == 0:
            reactionTimes[i] = 1700
    return reactionTimes, timeCodes, isCorrect


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
    plt.title(f'Reaction Time vs Time Code for {email} (Session: {sessionId}, Test: {testId})')
    plt.grid(True)
    plt.show()


# email = 'strasser@example.com'
# sessionId = 1
# testId = 2

# reactionTimes, timeCodes = getReactionTimesAndTimeCodes1out2(db_path, email, sessionId, testId)
def get_files_in_folder(folder_path):
        files = []
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                files.append(file)
        return files

def parseFileName(file):
    s = file.split('_')
    return s[0], s[1], s[2], s[3]

def getAllData(db_path):
    data = {}

    files = get_files_in_folder('./signaux EEG')
    # print(files)
    filenames_emails = {"Kayssieh":"kayssieh@example.com", "Revillon":"revillon@example.com", "Yvert":"yvert@example.com", "Strasser":"strasser@example.com"}
    for file in files:
        name, _, gameType, sessionId = parseFileName(file)
        email = filenames_emails[name]
        if gameType == "Congruent":
            testId = 1
        else:
            testId = 2
        sessionId = int(sessionId.split('.')[0])

        reactionTimes, timeCodes = getDataForSession(db_path, email, sessionId, testId)
        
        fileData = reactionTimes, timeCodes
        data[file] = fileData
    return data

def getRidDoublons(reactionTimes, timeCodes, isCorrect):
    
    reactionTimes = [reactionTimes[i*2] for i in range(len(reactionTimes)//2)]
    timeCodes = [timeCodes[i*2] for i in range(len(timeCodes)//2)]
    isCorrect = [isCorrect[i*2] for i in range(len(isCorrect)//2)]
    return reactionTimes, timeCodes, isCorrect

def separateApparitionXClickTimeCodes(reactionTimes, timeCodes, isCorrect):
    """On suppose que les doublons dus au double envoie des données ont été supprimé. La fonction renvoie la liste des time codes au moment de l'apparition des flèches ainsi qu'au moment du clique. La fonction renvoie écalement les reaction times des timescodes où il y a eu un clique, ie. enlève le dernier sinon."""
    appartionTC = []
    clickTC = []
    new_reactionTimes = []
    new_isCorrect = []
    j=0
    for i in range(len(reactionTimes)):
        if (j+1 < len(timeCodes)):
            new_reactionTimes.append(reactionTimes[i])
            new_isCorrect.append(isCorrect[i])
            if reactionTimes[i] != 1700:

                appartionTC.append(timeCodes[j])           
                clickTC.append(timeCodes[j+1])
                j+=2
            
            else:
                appartionTC.append(timeCodes[j])
                clickTC.append(timeCodes[j]+1700)
                j+=1
        else:
            break
    
            

    return new_reactionTimes, clickTC, new_isCorrect

def getTimeCodesOnClick(reactionTimes, timeCodes):
    
    timeCodes = [timeCodes[i*2+1] for i in range(len(timeCodes)//2)]
    reactionTimes = [reactionTimes[i] for i in range(len(reactionTimes)//2)]
    

    return reactionTimes, timeCodes

def getDataForSession(db_path, email, sessionId, testId):
    reactionTimes, timeCodes, isCorrect = getReactionTimesAndTimeCodesAndIsCorrect(db_path, email, sessionId, testId)
    # print(len(reactionTimes), len(timeCodes), len(isCorrect))
    reactionTimes, timeCodes, isCorrect = getRidDoublons(reactionTimes, timeCodes, isCorrect)
    # print(len(reactionTimes), len(timeCodes), len(isCorrect))
    reactionTimes, clickTimeCodes, isCorrect = separateApparitionXClickTimeCodes(reactionTimes, timeCodes, isCorrect)
    # print(len(reactionTimes), len(clickTimeCodes), len(isCorrect))
    reactionTimes, timeCodes, isCorrect = isNotCorrectTo1700(reactionTimes, clickTimeCodes, isCorrect)
    # print(len(reactionTimes), len(timeCodes), len(isCorrect))
    return reactionTimes, timeCodes

# files = get_files_in_folder(folder_path)
# print(files)
if __name__ == '__main__':
    # apparition, click = separateApparitionXClickTimeCodes(reactionTimes=[5,1700,1700,8], timeCodes=[1,6,7,10,7,9])
    # print(len(apparition))
    # print(len(click))


    db_path = './instance/attention.db'
    # data = getDataFileNamesXReactionTimesXTimesCodes(db_path)
    getDataForSession(db_path, "revillon@example.com", 1, 2)
    # data = getAllData(db_path)
    # print(data)


