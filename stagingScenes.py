#!/usr/bin/env python3
import pandas as pd

prefix = './movie_scripts/'
sufix = '.txt'
movieNames = ['Star Wars', 'Spider-man', 'The Matrix', 'The Lion King', 'Hunger Games']

movieStages = {
    'Star Wars': {
        'initiation': 'INT. TATOOINE - MOS EISLEY - CANTINA - INITIATION',
        'return': '',
    },
    'Spider-man': {
        'initiation': '',
        'return': '',
    },
    'The Matrix': {
        'initiation': 'INT.  HOVERCRAFT - INITIATION',
        'return': '',
    },
    'The Lion King': {
        'initiation': 'EXT. EDGE OF THE JUNGLE - DAY - INITIATION',
        'return': '',
    },
    'Hunger Games': {
        'initiation': '',
        'return': '',
    }
}

dataDir  = './data/base/'

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
        df = pd.read_csv('{}{}.csv'.format(dataDir, movieName))
        print(df)
        df = renameIndex(df)
        chars = set()
        lines = f.readlines()
        charsInScene = set()
        sceneCounter = 0
        for line in lines:
            line = line.replace('<b>', '').replace('</b>', '').replace('\t', '').strip()
            if line.startswith('INT') or line.startswith('EXT'):
                createEdges(df, charsInScene)
                charsInScene = set()
                sceneCounter = sceneCounter + 1
            else:
                if checkIsChar(line):
                    for char in df.columns:
                        if char in line:
                            charsInScene.add(char)
                            break
        df.to_csv('./data/dynamic/{}.csv'.format(movieName))   
        print(sceneCounter)

