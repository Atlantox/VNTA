import pickle

from core import *


filePath = ''
fileName = ''
fileFormat = ''
all_ways:list[ActionChain] = []  # The list of all ActionChain
all_decisions, novel_points = [], []
endings = {}  # Ending statistics


def run():
    global all_decisions, novel_points, fileName, filePath, fileFormat
    filePath = 'D:/Proyectos/VNTA/decisions.vnta'
    fileName, fileFormat = GetFileNameAndFormat(filePath)

    if fileFormat == '.csv':
        all_decisions, novel_points = ReadDecisions(filePath)
        CreateDecisionsTree()
    elif fileFormat == '.vnta':
        LoadDecisionsTree()  


def CreateDecisionsTree():
    crt_id = 0  # Current decision index

    while crt_id < len(all_decisions):
        currentDecision:Decision =  all_decisions[crt_id]

        if currentDecision.type == 'D':  # Decision
            ''' A decision consist in a situation and several posible options '''
            related_decisions = GetRelatedDecisions(currentDecision, crt_id)            

            crt_id += len(related_decisions) - 1 # Skipping the related decisions for the while loop
            i = 0

            if all_ways == []:
                # We insert the first decision, the begin of all paths
                for decision in related_decisions:                    
                    to_add = ActionChain([decision], novel_points).change_points(decision)
                    all_ways.append(to_add)

            else:
                # At least one path exists
                for i in range(len(all_ways)):
                    #  For each path we will try to take the current decision
                    if not all_ways[i].decision_is_compatible(currentDecision):
                        continue

                    original_way = all_ways[i].copy() # A copy of the current way before it changes                    

                    first = True
                    for decision in related_decisions:
                        if first:
                            # If is the first decision, the current path will take it
                            all_ways[i].take_decision(decision)
                            first = False
                        else:
                            # If not the first decision, a copy of the original way take the decision and appends it in all_ways
                            all_ways.append(original_way.copy().take_decision(decision))


        elif currentDecision.type == 'C':  # Consecuence
            ''' Consecuence decision consist in a decision that happen depending of a previous decision taked '''
            if all_ways == []:
                print(f'Consecuences needs a anterior decision in {currentDecision}')
            else:
                for way in all_ways:

                    if not way.decision_is_compatible(currentDecision):
                        continue
                    
                    way.take_decision(currentDecision)
                    '''
                    if '*-1-3-5-7-10-' in str(way):
                        print('ESTA\n')
                        print(currentDecision)
                        print(way, '\n')
                    '''

        elif currentDecision.type == 'I':   # If condition
            for way in all_ways:
                if not way.decision_is_compatible(currentDecision):
                        continue

                CheckCondition(way, currentDecision)

        elif 'ED-' in currentDecision.type:  # Endings
            for way in all_ways:
                if not way.decision_is_compatible(currentDecision):
                    continue
                
                if CheckCondition(way, currentDecision):
                    endingType = currentDecision.type.split('-')[1]
                    way.finish(endingType)
                    try:
                        endings[endingType] += 1
                    except KeyError:
                        endings[endingType] = 1
                        

        else:
            print(f'{currentDecision.id} decision has wrong type: {currentDecision.type}\nPlease use D, C, I or Ed-')

        crt_id += 1

    if fileFormat == '.csv':
        save_path = SaveDataInFile()

    print('Decision tree successfully created and saved in:', save_path)
    DisplayMenu()


def LoadDecisionsTree():
    '''
    If a .vnta file is given, all data is loaded from that file
    This function is usefull when you have a really really big decision tree
    '''
    global all_ways, novel_points, endings
    file = open(filePath, 'rb')
    data = pickle.load(file)
    file.close()

    all_ways = data['all_ways']
    novel_points = data['novel_points']
    endings = data['endings']
    print('Decision tree successfully loaded')
    DisplayMenu()


def SaveDataInFile():
    '''
    Once created the decision tree, it is saved in a file to prevent to create another equal decision tree 
    Returns the path of the created .vnta file
    '''
    new_path = filePath.replace(fileName + fileFormat, fileName + '.vnta')
    file = open(new_path, 'wb')
    to_save = {
        'all_ways': all_ways,
        'novel_points': novel_points,
        'endings': endings
    }
    pickle.dump(to_save, file)
    file.close()
    return new_path


def GetRelatedDecisions(decision, crt_id):
    ''' Get a decision and all the next related decisions '''
    i = 1
    related_decisions = [decision]
    while decision.name == all_decisions[crt_id + i].name:
        related_decisions.append(all_decisions[crt_id + i])
        i += 1
        if crt_id + i >= len(all_decisions): break
    
    return related_decisions


def DisplayMenu():
    ''' Shows a menu to get useful data about the decision tree '''

    commands = {
        '1': DisplayTotals,
        '2': DisplayAllRoads,
        '3': DisplaySearch
    }

    header = '#########    [V]isual  [N]ovel  [T]echnical  [A]ssistant    #########'
    Atlantox = '- By Atlantox -'
    print('#' * len(header))
    print(header)
    halfs = {
        'A': int(len(Atlantox) / 2),
        'H': int(len(header) / 2)
        }
    space = '#' * (halfs['H'] - halfs['A'])
    print(space + Atlantox + space)
    print('#' * len(header))
    while True:
        print('''
        [1]: Display endings statistics.
        [2]: Display all posible roads.
        [3]: Search road.
        [0]: Exit.
        ''')
        com = input('Select the command you want to execute: ').strip()

        if com in commands.keys():
            commands[com]()
        else:
            if com == '0': break

            print('Wrong command')


def DisplayTotals():
    ''' Show road number and percents of each ending '''
    global all_ways
    all_ways = GetSortedActionChain(all_ways)

    print('Total ways:', len(all_ways))

    totals = GetEndingStatistics(endings, len(all_ways))

    if 'good' in endings.keys():
        prob = (endings['good'] * 100) / len(all_ways)
        totals += f'\nGood ending probability: {prob}%\nNot-good ending probability: {100 - prob}%'

    print(totals)


def DisplayAllRoads():
    ''' Display all roads showing code, ending and novel points of each one '''
    for way in all_ways:
        print(way.summary(1))
    print('\n')


def DisplaySearch():
    ''' Displays the search submenu (search by code and novel points) '''
    pass


def DisplaySearchByCode():
    ''' Search for roads by their code '''
    print('Search are made by the road code, example: *-1-3-8-12-22-* ending type')
    print('Any coincidence will be displayed with some statistics values')
    print('')
    search = input('Please, insert the search: ').strip()

    results = []
    search_endings = {k:0 for k in endings.keys()} | {'unfinished': 0}
    for way in all_ways:
        if search in str(way):
            results.append(way)
            if way.finished is not None:
                search_endings[way.finished] += 1

    if results != []:
        for way in results:
            print(way)
        
        print('\n\nRoads found:', len(results))
        to_show = GetEndingStatistics(search_endings, len(results))
        print(to_show)
    else:
        print(f'Not results for {search} found')


def DisplaySearchByPoints():
    ''' Search for roads by a specific condition '''
    pass


if __name__ == '__main__':
    run()