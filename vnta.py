import pickle

from core import *

# id, type, name, option, dependency, comment, friendship, qualification

filePath = ''
fileName = ''
fileFormat = ''
all_ways:list[ActionChain] = []  # The list of all ActionChain
all_decisions, novel_points = [], []
endings = {}  # Ending statistics

def run():
    global all_decisions, novel_points, fileName, filePath, fileFormat
    filePath = 'D:/Proyectos/VNTA/decisions.csv'
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
            ''' A decision consist in  '''
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
                    if not all_ways[i].decision_is_compatible(currentDecision):
                        continue

                    way.take_decision(currentDecision)

        elif currentDecision.type == 'I':   # If condition
            for way in all_ways:
                if not all_ways[i].decision_is_compatible(currentDecision):
                        continue

                CheckCondition(way, currentDecision)

        elif 'ED-' in currentDecision.type:  # Endings
            for way in all_ways:
                if not all_ways[i].decision_is_compatible(currentDecision):
                        continue
                
                if CheckCondition(way, currentDecision):
                    way.finish()

                    endingType = currentDecision.type.split('-')[1]
                    try:
                        endings[endingType] += 1
                    except KeyError:
                        endings[endingType] = 1
                        

        else:
            print(f'{currentDecision.id} decision has wrong type: {currentDecision.type}\nPlease use D, C, I or Ed-')

        crt_id += 1

    if fileFormat == '.csv':
        SaveDataInFile()

    DisplayTotals()

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
    DisplayTotals()


def DisplayMenu():
    ''' Shows a menu to get useful data about the decision tree '''
    while True:
        print('Mostrando menú')


def SaveDataInFile():
    ''' Once created the decision tree, it is saved in a file to prevent to create another equal decision tree '''
    new_path = filePath.replace(fileName + fileFormat, fileName + '.vnta')
    file = open(new_path, 'wb')
    to_save = {
        'all_ways': all_ways,
        'novel_points': novel_points,
        'endings': endings
    }
    pickle.dump(to_save, file)
    file.close()


def GetRelatedDecisions(decision, crt_id):
    ''' Get a decision and all the next related decisions '''
    i = 1
    related_decisions = [decision]
    while decision.name == all_decisions[crt_id + i].name:
        related_decisions.append(all_decisions[crt_id + i])
        i += 1
        if crt_id + i >= len(all_decisions): break
    
    return related_decisions

def DisplayTotals():
    ''' Show ways number and percents of each ending '''
    global all_ways
    all_ways = GetSortedActionChain(all_ways)

    #for way in all_ways:
        #print(way, '····', way.points)

    print('Total ways:', len(all_ways))

    totals = f'\nTotal endings:\n'
    for key, value in endings.items():
        percent = (value * 100) / len(all_ways)
        totals += f'   {key}: {value} -> {percent}% -> {percent / 100} \n'

    print(totals)

if __name__ == '__main__':
    run()