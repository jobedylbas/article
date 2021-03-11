#!/usr/bin/env python3
import pandas as pd
import regex as re

prefix = './movie_scripts/'
sufix = '.txt'
movieNames = ['Star Wars', 'The Matrix', 'The Lion King', 'Hunger Games']

dataDir  = './data/base/'

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
    for char in char:
        line.replace(char, '')
    return line.replace('-', ' ').lower().strip()

def renameIndex(df):
    dic = {}
    for row in df.index:
        dic[row] = df.columns[row+1]
    df = df.drop(columns = ['Unnamed: 0'])
    df = df.rename(index=dic)
    return df

for movieName in movieNames:
    with open('{}{}{}'.format(prefix, movieName, sufix), 'r') as f:
        df = pd.read_csv('{}{}.csv'.format(dataDir, movieName))
        df = renameIndex(df)
        chars = set()
        lines = f.readlines()
        charsInScene = set()
        sceneCounter = 0
        for line in lines:
            line = line.replace('<b>', '').replace('</b>', '').replace('\t', '').replace(':', ' ').replace(',', ' ')
            line = line.replace(';', ' ').replace('?', ' ').replace('!', ' ').replace('\'s', '').replace('\'', '')
            line = line.replace('-', ' ').lower().strip()
            if line != '':
                # print(line)
                if line.startswith('int.') or line.startswith('ext.'):
                    createEdges(df, charsInScene)
                    charsInScene = set()
                    sceneCounter = sceneCounter + 1
                else:
                    splitedLine = line.replace('.', ' ').split(' ')
                    for char in df.columns:
                        if char.lower() == line:
                            charsInScene.add(char)
                            break
                    for char in df.columns:
                        if ' ' in char:
                            if (char.lower() in line):
                                charsInScene.add(char)
                                break
                        else: 
                            if (char.lower() in line.split(' ')):
                                charsInScene.add(char)
                                break
        createEdges(df, charsInScene)
        sceneCounter = sceneCounter + 1
        df.to_csv('./data/static/{}.csv'.format(movieName))   
        print(sceneCounter)

