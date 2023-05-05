from ActionChain import ActionChain
from Decision import Decision

def GetFileNameAndFormat(path:str):
    fileFullName = path.split('/')[-1]  # File name with format
    splits = fileFullName.split('.')
    fileFormat = '.' + splits[-1]

    fileName = ''
    for split in splits[:-1]:
        fileName += split
    
    return fileName, fileFormat


def ReadDecisions(filePath):
    ''' Return all decisions in the specified file and the novel points '''
    decisions = []
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    
    novel_points = [l.strip() for l in lines[0].split(';')[6:]]

    for line in lines[1:]:
        if line.strip() == '':
            continue

        splits = [s.strip() for s in line.split(';')]
        to_add = []
        for split in splits[:6]:
            if split == '':
                split = None
            to_add.append(split)

        points = []
        for split in splits[6:]:
            points.append(None) if split == '' else points.append(int(split)) 

        decisions.append(Decision(
            id=to_add[0],
            type=to_add[1],
            name=to_add[2],
            option=to_add[3],
            comment=to_add[4],
            dependency=to_add[5],
            points=points,
        ))
        
    return decisions, novel_points


def CheckCondition(way:ActionChain, decision:Decision):
    i = 0
    decision_taked = False
    for operator in decision.option.split(','):
        while decision.points[i] is None:
            i += 1
        
        if ConditionIsRight(way.get_points_as_list()[i], operator, decision.points[i]):
            way.take_decision(decision, False)
            decision_taked = True
        i += 1

    return decision_taked


def ConditionIsRight(left, operator, right):
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


def GetSortedActionChain(ways:list[Decision]):
    decisions = {}
    sortedDecisions = []
    for way in ways:
        decisions[str(way)] = way

    keys = list(decisions.keys())
    keys.sort()
    for d in keys:
        sortedDecisions.append(decisions[d])

    return sortedDecisions