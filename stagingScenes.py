#!/usr/bin/env python3
import pandas as pd

prefix = './movie_scripts/'
sufix = '.txt'
movieNames = ['Star Wars', 'The Matrix', 'The Lion King', 'Hunger Games']

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

def formatLine(line):
    chars = ['<b>', '</b>', '\t', ':', ',', ';', '?', '!', '\'s', '\'', '-']
    for char in chars:
        line = line.replace(char, '')
    return line.replace('-', ' ').upper().strip()

def renameIndex(df):
    dic = {}
    for row in df.index:
        # print(df.columns[row+1])
        dic[row] = df.columns[row+1]
    df = df.drop(columns = ['Unnamed: 0'])
    df = df.rename(index=dic)
    print(df)
    return df

def stageChanged(line):
    if ('INITIATION' in line) or ('ROAD BACK' in line): 
        return True
    else:
        return False

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
        for line in lines:
            line = formatLine(line)
            # print(line)
            if stageChanged(line):
                createEdges(df_splited, charsInScene)
                df_splited.to_csv('./data/dynamic/{}/{}.csv'.format(movieName, getStage(stage)))
                
                df_splited = pd.read_csv('{}{}.csv'.format(dataDir, movieName))
                
                df_splited = renameIndex(df_splited)
                charsInScene = set()
                print(stage)
                print(sceneCounter)
                stage = stage + 1
                sceneCounter = 0
                
            elif line.startswith('INT.') or line.startswith('EXT.'):
                createEdges(df_splited, charsInScene)
                charsInScene = set()
                sceneCounter = sceneCounter + 1
            else:
                splitedLine = line.replace('.', ' ').split(' ')
                for char in df_splited.columns:
                    if char == line:
                        charsInScene.add(char)
                        break
                for char in df_splited.columns:
                    if char.lower() in line.split(' '):
                        charsInScene.add(char)
                        break
                    elif 'ed' not in char: 
                        if (char.lower() in line):
                            charsInScene.add(char)
                            break
        sceneCounter = sceneCounter + 1
        createEdges(df_splited, charsInScene)
        df_splited.to_csv('./data/dynamic/{}/{}.csv'.format(movieName, getStage(stage)))
        print(getStage(stage), sceneCounter)

