#!/usr/bin/env python3
import pandas as pd

prefix = './movie_scripts/'
sufix = '.txt'
movieNames = ['Star Wars', 'The Matrix', 'The Lion King']

movieStages = {
    'Star Wars': {
        'initiation': 'INT. TATOOINE - MOS EISLEY - CANTINA - INITIATION',
        'return': 'INT. MASSASSI OUTPOST - MAIN HANGAR DECK - ROAD BACK',
    },
    'Spider-man': {
        'initiation': '',
        'return': '',
    },
    'The Matrix': {
        'initiation': 'INT.  HOVERCRAFT - INITIATION',
        'return': 'INT.  "EL" STATION (MATRIX) - DAY - ROAD BACK',
    },
    'The Lion King': {
        'initiation': 'EXT. EDGE OF THE JUNGLE - DAY - INITIATION',
        'return': 'EXT. REFLECTING POOL - NIGHT - ROAD BACK',
    },
    'Hunger Games': {
        'initiation': '',
        'return': '',
    }
}

dataDir  = './data/base/'

def getStage(flag):
    if flag == 0:
        return 'departure'
    elif flag == 1:
        return 'initiation'
    else:
        return 'return'

def createEdges(df, chars):
    # print(zip(chars, chars))
    charList = list(chars)
    for i in range(0, len(charList)):
        for char in charList[i:]:
            if char != charList[i]:
                df.at[char, charList[i]] = df.at[char, charList[i]] + 1
                df.at[charList[i], char] = df.at[charList[i], char] + 1

def checkIsChar(line):
    spaceCounter = 0
    for char in line:
        if char == ' ':
            spaceCounter = spaceCounter + 1
        if spaceCounter > 3:
            return False
    return True

def renameIndex(df):
    dic = {}
    for row in df.index:
        # print(df.columns[row+1])
        dic[row] = df.columns[row+1]
    df = df.drop(columns = ['Unnamed: 0'])
    df = df.rename(index=dic)
    # print(df)
    return df

for movieName in movieNames:
    with open('{}{}{}'.format(prefix, movieName, sufix), 'r') as f:
        df_splited = pd.read_csv('{}{}.csv'.format(dataDir, movieName))
        # print(df)
        df_splited = renameIndex(df_splited)
        chars = set()
        lines = f.readlines()
        charsInScene = set()
        sceneCounter = 0
        stage = 0
        print('\n' +movieName)
        for line in lines:
            line = line.replace('<b>', '').replace('</b>', '').replace('\t', '').strip()
            if line in movieStages[movieName].values():
                df_splited.to_csv('./data/dynamic/static/{}/{}.csv'.format(getStage(stage), movieName))
                print(getStage(stage), sceneCounter)
                
                df_splited = pd.read_csv('{}{}.csv'.format(dataDir, movieName))
                df_splited = renameIndex(df_splited)
                charsInScene = set()
                stage = stage + 1
                sceneCounter = 0
            elif line.startswith('INT') or line.startswith('EXT'):
                createEdges(df_splited, charsInScene)
                charsInScene = set()
                sceneCounter = sceneCounter + 1
            else:
                if checkIsChar(line):
                    for char in df_splited.columns:
                        if char in line:
                            charsInScene.add(char)
                            break
        createEdges(df_splited, charsInScene)
        df_splited.to_csv('./data/dynamic/static/{}/{}.csv'.format(getStage(stage), movieName))
        print(getStage(stage), sceneCounter)

