import pickle

from tkinter import messagebox

from core.utils import *


AVAILABLE_FORMATS = ['.csv', '.xlsx']
filePath = ''
fileName = ''
fileFormat = ''
all_ways:list[ActionChain] = []  # The list of all ActionChain
all_decisions, novel_points = [], []
endings = {}  # Ending statistics


def StartDecisionsTree(path):
    ''' Reset all the global variables and Create or load the decision tree if exists '''
    global all_decisions, novel_points, fileName, filePath, fileFormat, all_ways, endings
    all_ways, all_decisions, novel_points = [], [], [] # Cleaning global variables
    endings = {}
    filePath = path
    fileName, fileFormat = GetFileNameAndFormat(filePath)

    if fileFormat in AVAILABLE_FORMATS:
        all_decisions, novel_points = ReadDecisions(filePath, fileFormat)
        CreateDecisionsTree()
    elif fileFormat == '.vnta':
        LoadDecisionsTree()  

    return all_decisions, all_ways, endings, novel_points


def CreateDecisionsTree():
    ''' Each Decision branches the start point creating a tree of Decisions '''
    crt_id = 0  # Current decision index

    ways_idLists = []
    total_combinations = 1
    counter = 0
    brancher_decisions = []

    while crt_id < len(all_decisions):
        currentDecision:Decision =  all_decisions[crt_id]

        if currentDecision.type == 'D':
            counter+=1 
            related_decisions = GetRelatedDecisions(currentDecision, crt_id)
            options = []
            for option in [op.option for op in related_decisions]:
                options.append({
                    'name':option
                })

            brancher_decisions.append({
                'name':related_decisions[0].name,
                'options': options
                })

            possible_options = len(related_decisions)
            total_combinations *= possible_options
            crt_id += possible_options - 1

        crt_id += 1

    print('total:', total_combinations)
    print('counter:',counter)

    aux = total_combinations
    for decision in brancher_decisions:
        aux /= len(decision['options'])
        for option in decision['options']:
            option['times'] = int(aux)

    for d in brancher_decisions:
        print(d['name'], d['options'], '\n')

    return


    while crt_id < len(all_decisions):
        currentDecision:Decision =  all_decisions[crt_id]

        if currentDecision.type == 'D':  # Decision
            ''' A decision consist in a situation and several possible options '''
            related_decisions = GetRelatedDecisions(currentDecision, crt_id)            

            crt_id += len(related_decisions) - 1 # Skipping the related decisions for the while loop
            i = 0

            if all_ways == []:
                # We insert the first decision, the begin of all paths
                for decision in related_decisions:                    
                    to_add = ActionChain([decision], novel_points).change_points(decision)
                    # Creating a ACtionChain and setting the initial novel points
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
            ''' Consecuence decision consist in a decision that happen depending of a previous decision taken '''
            if all_ways == []:
                messagebox.showerror('Decision type error', f"Decision '{currentDecision.id}' type cannot be C without a previous Decision")
                raise KeyError('Incorrect C decision type usage')
            else:
                for way in all_ways:
                    if not way.decision_is_compatible(currentDecision):
                        continue  # If not compatible, continue in the next way
                    
                    way.take_decision(currentDecision)

        elif currentDecision.type == 'I':   # If condition
            '''
            An if condition Decision is taken only if the current road have the requeriments
            The conditions are bassed in novel points
            '''
            for way in all_ways:
                if not way.decision_is_compatible(currentDecision):
                        continue  # If not compatible, continue in the next way

                CheckCondition(way, currentDecision)

        elif 'E-' in currentDecision.type:  # Endings
            '''
            An ending can depend of 2 things, by novel points and/or a previous Decision
            if the road meets the condition, that road ends
            '''
            for way in all_ways:
                available_to_take = False
                if not way.decision_is_compatible(currentDecision):
                    continue  # If not compatible, continue in the next way
                
                if novel_points == []:
                    #  If the novel's decisions doesn't have points
                    available_to_take = True
                else:
                    #  If the novel's decisions have points, check the condition
                    if CheckCondition(way, currentDecision):
                        available_to_take = True

                if available_to_take:
                    endingType = currentDecision.type.split('-')[1]
                    way.finish(endingType)

                    try:
                        endings[endingType] += 1
                    except KeyError:
                        endings[endingType] = 1



                        
        else:
            messagebox.showerror('Decision type error', f"Decision '{currentDecision.id}' has wrong type: {currentDecision.type}\nPlease use D, C, I or E-")
            raise KeyError('Unknown decision type usage')

        crt_id += 1
        #print(len(all_ways))

    if fileFormat in AVAILABLE_FORMATS:
        '''
        In cases of you have a really big list of decisions, with a
        really big list of possible roads, these roads, novel points and decisions
        are saved in a .vnta file to save processor effort in the next time
        .vnta files can be opened by the same program
        '''
        save_path = SaveDecisionsTree()

    messagebox.showinfo('Success', 'Decision tree successfully created and saved in: ' + save_path)


def SaveDecisionsTree():
    '''
    Once created the decision tree, it is saved in a file to prevent to create another equal decision tree
    really useful if you have a really big list of decisions
    Returns the path of the created .vnta file
    '''
    new_path = filePath.replace(fileName + fileFormat, fileName + '.vnta')
    
    file = open(new_path, 'wb')

    to_save = {
        'all_ways': all_ways,
        'all_decisions': all_decisions,
        'novel_points': novel_points,
        'endings': endings
    }

    pickle.dump(to_save, file)
    file.close()
    return new_path


def LoadDecisionsTree():
    '''
    If a .vnta file is given, all data is loaded from that file
    This function is usefull when you have a really really big decision tree
    '''
    file = open(filePath, 'rb')
    data = pickle.load(file)
    file.close()

    for w in data['all_ways']: all_ways.append(w)
    for p in data['novel_points']: novel_points.append(p)
    for e, v in data['endings'].items(): endings[e] = v
    for d in data['all_decisions']: all_decisions.append(d)

    messagebox.showinfo('Success', 'Decision tree successfully loaded')


def GetRelatedDecisions(decision, crt_id):
    ''' Get a decision and all the next decisions with same name '''
    i = 1
    related_decisions = [decision]
    while decision.name == all_decisions[crt_id + i].name:
        related_decisions.append(all_decisions[crt_id + i])
        i += 1
        if crt_id + i >= len(all_decisions): break
    
    return related_decisions


def GetDecisionsBySearch(search_type:str, search:str = ''):
    '''
    Return a list of the Decisions depending of a search
    search can be by 'id', 'name', 'option', 'dependency' and 'points'
    do a '*' search to get all Decisions
    '''
    if search == '*':
        return all_decisions

    results = []
    items = [v.strip() for v in search.split(',') if v != '']
    if search_type == 'id':
        for d in all_decisions:
            if d.id in items: results.append(d)                

    elif search_type == 'name':
        for d in all_decisions:
            for name in items:
                if name in d.name:
                    results.append(d)
                    break
                
    elif search_type == 'option':
        for d in all_decisions:
            for option in items:
                if d.option is not None:
                    if option in d.option:
                        results.append(d)
                        break

    elif search_type == 'dependency':
        for d in all_decisions:
            for dependency in items:
                if d.dependencies is not None:
                    if dependency in d.dependencies:
                        results.append(d)
                        break

    elif search_type == 'points':
        indexes = []
        for point in items:
            for i, real_point in enumerate(novel_points):
                if point == real_point: 
                    indexes.append(i)
                    break

        if indexes != []:
            for d in all_decisions:
                pointOK = True
                # Checking if decision affects targets points
                for index in indexes:
                    if d.points[index] is None:
                        pointOK = False
                        break

                if pointOK:
                    results.append(d)

    if results == []: results = None

    return results


def GetRoadsBySearch(search_type:str, search:str):
    '''
    Returns a list of ActionChain depending of a search criterium
    can be by 'code', 'ending' and 'points'
    do a search with '*' to get all roads
    '''
    if search == '*': return all_ways

    results = []
    if search_type == 'code':
        codes = [s.strip() for s in search.split(',') if s != '']

        for way in all_ways:
            coincidance = True
            for code in codes:
                
                if code not in str(way):
                    coincidance = False
                    break

            if coincidance: results.append(way)     

    elif search_type == 'ending':
        criterions = [s.strip() for s in search.split(',') if s != '']

        for way in all_ways:
            if way.finished is None:
                continue
            if way.finished in criterions:
                results.append(way)

    elif search_type == 'points':
        conditions = search.split(',')
        for way in all_ways:
            conditionOK = True
            for condition in conditions:
                point, operator, value = condition.strip().split(' ')
                currentPoint = int(way.points[point])
                if not ConditionIsRight(currentPoint, operator, int(value)):
                    conditionOK = False
                    break

            if conditionOK:
                results.append(way)

    if len(results) == 0:
        results = None

    return results