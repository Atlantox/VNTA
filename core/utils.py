from core.ActionChain import ActionChain
from core.Decision import Decision

def GetFileNameAndFormat(path:str):
    ''' Get a file path and returns the file name without format, and the file format '''
    fileFullName = path.split('/')[-1]  # File name with format
    splits = fileFullName.split('.')
    fileFormat = '.' + splits[-1]

    fileName = ''
    for split in splits[:-1]:
        fileName += split
    
    return fileName, fileFormat


def ReadDecisions(filePath):
    ''' Return all decisions in the specified .csv file and the novel points '''
    decisions = []
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    
    novel_points = [l.strip() for l in lines[0].split(';')[5:]]

    for line in lines[1:]:
        if line.strip() == '':
            continue

        splits = [s.strip() for s in line.split(';')]
        to_add = []
        for split in splits[:5]:
            if split == '':
                split = None
            to_add.append(split)

        if to_add[4] is not None:
            # If the decision has dependency, convert the stirng into a list
            dependencies = [s.strip() for s in to_add[4].split(',') if s != '']
            to_add[4] = dependencies            

        points = []
        for split in splits[5:]:
            points.append(None) if split == '' else points.append(int(split)) 

        decisions.append(Decision(
            id=to_add[0],
            type=to_add[1],
            name=to_add[2],
            option=to_add[3],
            dependencies=to_add[4],
            points=points,
        ))
        
    return decisions, novel_points


def CheckCondition(way:ActionChain, decision:Decision):
    '''
    Get a conditional Decision and an ActionChain
    Return True if the Decision was taken, otherwise return False
    '''
    i = 0
    decision_taken = False
    for operator in decision.option.split(','):
        while decision.points[i] is None:
            i += 1
        
        if ConditionIsRight(way.get_points_as_list()[i], operator, decision.points[i]):
            way.take_decision(decision, False)
            decision_taken = True
        i += 1

    return decision_taken


def ConditionIsRight(left, operator, right):
    ''' Return True if (left operator right), otherwise return False'''
    result = False
    if right is not None:
        if operator == '<':
            if left < right:
                result = True
        if operator == '<=':
            if left <= right:
                result = True
        if operator == '>':
            if left > right:
                result = True
        if operator == '>=':
            if left >= right:
                result = True
        if operator == '=':
            if left == right:
                result = True

    return result


def GetSortedActionChain(ways:list[ActionChain]):
    ''' Gets a list of ActionChain and returns it sorted by id '''
    decisions = {}
    sortedDecisions = []
    for way in ways:
        decisions[str(way)] = way

    keys = list(decisions.keys())
    keys.sort()
    for d in keys:
        sortedDecisions.append(decisions[d])

    return sortedDecisions


def GetEndingStatistics(endings:dict, roads:int):
    ''' Return a string with statistics of endings given '''
    #result = 'Endings statistics\n'
    result = {}
    for key, value in endings.items():
        percent = (value * 100) / roads
        to_add = {
            'count': value,
            'percent': percent,
            'index': percent / 100
        }
        result[key] = to_add
        #result += f'   {key}: {value} ··· {percent}% ··· {percent / 100} \n'
    return result