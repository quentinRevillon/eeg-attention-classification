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
    return reactionTimes, timeCodes


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

def getRidDoublons(reactionTimes, timeCodes):
    
    reactionTimes = [reactionTimes[i*2] for i in range(len(reactionTimes)//2)]
    timeCodes = [timeCodes[i*2] for i in range(len(timeCodes)//2)]
    
    return reactionTimes, timeCodes

def getTimeCodesOnClick(reactionTimes, timeCodes):
    
    timeCodes = [timeCodes[i*2+1] for i in range(len(timeCodes)//2)]
    reactionTimes = [reactionTimes[i] for i in range(len(reactionTimes)//2)]
    

    return reactionTimes, timeCodes

def getDataForSession(db_path, email, sessionId, testId):
    reactionTimes, timeCodes, isCorrect = getReactionTimesAndTimeCodesAndIsCorrect(db_path, email, sessionId, testId)
    reactionTimes, timeCodes = isNotCorrectTo1700(reactionTimes, timeCodes, isCorrect)
    reactionTimes, timeCodes = getRidDoublons(reactionTimes, timeCodes)
    reactionTimes, timeCodes = getTimeCodesOnClick(reactionTimes, timeCodes)
    return reactionTimes, timeCodes

# files = get_files_in_folder(folder_path)
# print(files)
if __name__ == '__main__':
    db_path = './instance/attention.db'
    # data = getDataFileNamesXReactionTimesXTimesCodes(db_path)
    getDataForSession(db_path, "revillon@example.com", 1, 2)
    data = getAllData(db_path)
    print(data)


