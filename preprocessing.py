#!/usr/bin/env python3
import pandas as pd
prefix = './movie_scripts/'
sufix = '.txt'
movieNames = ['Star Wars', 'Spider-man', 'The Matrix', 'The Lion King', 'Hunger Games']

dataDir  = '../data/'
APIprefix = 'https://api.themoviedb.org/3/movie/'
movieIds = [ '11'] #, '557', '603', '70160', '607'] # Spiderman, Matrix, Star Wars, Hunger Games, MIB
castAttr = '/credits'
APIsufix = '?api_key=fb61737ab2cdee1c07a947778f249e7d&language=en-US'

def createRelationshipMatrix(charNames: list, movieId: str):
    """Create a csv file that represents the relation between the movie characters

    Args:
        charNames (list): List of characters names of the movie
        movieId (str): Id of the movie in the TMDB
    """
    with open('{}relations/{}_relations.csv'.format(dataDir, movieId), 'w', encoding='utf-8') as relations:
        with open('{}relation_types/{}_relations_types.csv'.format(dataDir, movieId), 'w', encoding='utf-8') as relationsTypes:
                relations.write('chars,{}\n'.format(','.join(charNames)))
                relationsTypes.write('chars,{}\n'.format(','.join(charNames)))
                for name in charNames:
                    relationsTypes.write(name+',\n')
                    relations.write(name+',\n')

def createCharactersInfos(chars: list, movieId: str):
    """Create a csv file that represents all characters with its gender and archetypes

    Args:
        chars (list): A list of chars with its own gender and archetypes
        movieId (str): Id of the movie in the TMDB
    """ 
    with open('{}archetypes/{}_characters.csv'.format(dataDir, movieId), 'w', encoding='utf-8') as csv:
        csv.write('movie_id, character_name, gender, archetype\n')
        
        for char in chars:
            csv.write(char)

def replacing(line):
    replaces =[':', '(V.O.)', '(S.O.)', '(V.O)', '(V.O)', '(S.O)', '\'S VOICE', 'POV', '(O.S.)', '(TOGETHER)', '\'S', 'VOICE', 'WITH', '"', ',']
    for re in replaces:
        line = line.replace(re, '')
    return line.strip()

def spaces(line):
    spaceCounter = 0
    for char in line:
        if char == ' ':
            spaceCounter = spaceCounter + 1
        if spaceCounter > 3:
            return False
    return True

def isChar(line):
    if line.endswith('.'):
        return False
    if line.endswith(')') and line.startswith('('):
        return False
    checkChars = ['SEQ', '!', '?', '-', '(CONTINUED)', '[ALT']
    for char in checkChars:
        if char in line:
            return False
    return True
    

for movieName in movieNames:
    with open('{}{}{}'.format(prefix, movieName, sufix), 'r') as f:
        chars = set()
        lines = f.readlines()
        sceneState = 0
        sceneCounter = 0
        for line in lines:
            line = line.replace('<b>', '').replace('</b>', '').replace('\t', '').strip()
            if line.startswith('INT') or line.startswith('EXT'):
                sceneCounter = sceneCounter + 1
            elif line.isupper() and sceneCounter > 0:
                char = replacing(line)
                if spaces(line) and isChar(line):
                    charSplited = char.split('/')
                    if len(charSplited) > 1:
                        for c in charSplited:
                            chars.add(c)
                    else:
                        charSplited = char.split('&')
                        if len(charSplited) > 1:
                            chars.add(charSplited[0])
                            chars.add(charSplited[1])
                        else:
                            charSplited = char.split('AND')
                            if len(charSplited) > 1:
                                chars.add(charSplited[0])
                                chars.add(charSplited[1])
                            else: 
                                chars.add(char.strip())
        # Dic to create dataframe
        dic = {}
        for name in chars:
            if name != '':
                dic[name] = [0] * (len(chars)-1)
        # Create Dataframe
        d = pd.DataFrame(data=dic)
        # Remove duplicates
        d = d.drop(list(range(len(dic.keys()), len(d.index))))
        d = d.rename(index= lambda s: d.columns[s])
        d.to_csv('./data/base/{}.csv'.format(movieName))

        print(chars)
        print(movieName, sceneCounter)