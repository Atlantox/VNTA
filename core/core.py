import pickle

from tkinter import messagebox

from core.utils import *


AVAILABLE_FORMATS = ['.csv', '.xlsx']
filePath = ''
fileName = ''
fileFormat = ''
all_ways:list[ActionChain] = []  # The list of all ActionChain
all_decisions, novel_points = [], []
total_combinations = 1
endings = {}  # Ending statistics


def StartDecisionsTree(path):
    ''' Reset all the global variables and Create or load the decision tree if exists '''
    global all_decisions, novel_points, fileName, filePath, fileFormat, all_ways, endings, total_combinations
    all_ways, all_decisions, novel_points = [], [], [] # Cleaning global variables
    endings = {}
    filePath = path
    fileName, fileFormat = GetFileNameAndFormat(filePath)

    if fileFormat in AVAILABLE_FORMATS:
        all_decisions, novel_points, total_combinations = ReadDecisions(filePath, fileFormat)
        CreateDecisionsTree()
    elif fileFormat == '.vnta':
        LoadDecisionsTree()  

    return all_decisions, all_ways, endings, novel_points

#counter = 0

def explore_decision_tree(decisions:list[Decision], current_path:ActionChain, all_paths:list):
    #for d in decisions: print(d)
    #print()
    if current_path == []:
        current_path = ActionChain(points=novel_points)
    print('recibe', current_path)

    if not decisions:
        print('añade', current_path, '\n')
        #print(current_path)
        #global counter
        all_paths.append(current_path.copy())
        #counter += 1
        #print(counter)
        
        return

    current_decision = decisions[0]
    remaining_decisions = decisions[1:]
    original_path = current_path.copy()
    print('copia', original_path)

    for option in current_decision.options:
        #print(option)
        #if not current_path.option_is_compatible(option):
            #continue

        if current_decision.type == 'D':
            pass
        elif current_decision.type == 'C':
            pass
        elif current_decision.type == 'I':
            pass
        elif 'E-' in current_decision.type:
            endingType = current_decision.type.split('-')[1]
            current_path.finish(endingType)
        
        print(current_path, 'toma decision', option)

        #new_path = original_path.copy().take_option(option)
        #new_path.take_option(option)
        
        #current_path + [option.id]
        explore_decision_tree(remaining_decisions, original_path.copy().take_option(option), all_paths)



def CreateDecisionsTree():
    ''' Each Decision branches the start point creating a tree of Decisions '''
    crt_id = 0  # Current decision index
    InitDecisionTree()
    firsts_options = all_decisions[0].options
    firsts_ids = [o.id for o in firsts_options]
    current_combinations = int(total_combinations / len(firsts_options))
    print(total_combinations)

    roads = []

    explore_decision_tree(all_decisions, [], roads)

    for r in roads: print(r)



    return

    roads = []
    for id in firsts_ids:
        roads += [id + ','] * int(total_combinations / len(firsts_options))
    #print(len(roads))
    r_id = 0
    count = 0
    for decision in all_decisions[1:]:
        print(decision.name)
        if decision.type == 'D':
            current_combinations /= len(decision.options)
            o_id = 0

            while True:
                #print(r_id)
                to_add = roads[r_id] + decision.options[o_id].id + ','
                #print(f'{r_id}:{r_id+int(current_combinations)} -> {decision.options[o_id].name}')

                roads[r_id:r_id+int(current_combinations)] = [to_add] * int(current_combinations)

                r_id += int(current_combinations)
                if r_id == len(roads):
                    r_id = 0
                    #print('rompe aquí')
                    break
                o_id += 1
                if o_id == len(decision.options): o_id = 0
                count += 1
                print(count)
                if count >= len(roads):
                    #print('rompe acá')
                    break
                '''
                count += 1
                if count == current_combinations:
                    o_id += 1
                    if o_id == len(decision.options): o_id = 0
                    count = 0
                
                #print(current_combinations)
                if r_id == len(roads):  
                    break
                '''
        

    print('\n')
    for r in roads: print(r)
    print('decisiones', len(all_decisions))
    print('caminos', total_combinations)
    print('caminos reales', len(roads))


    '''

    left_priority = True
    roads_left = total_combinations
    final_roads = []

    
    currentRoad = ActionChain(points=novel_points)
    initial_ids = list(range(0, len(all_decisions[0].options)))
    cycles = len(initial_ids)
    initial_position = 1


    while(roads_left > 0):
        first_decision = True
        for decision in all_decisions:
            
            if decision.type == 'D':
                if first_decision:
                    first_decision = False
                    cycles -= 1
                    if cycles == 0:
                        cycles = len(initial_ids)
                        left_priority = not left_priority
                    if len(initial_ids) == 2:
                        if initial_position == 0: initial_position = 1
                        elif initial_position == 1: initial_position = 0
                    else:
                        if left_priority:
                            initial_position += 1
                            if initial_position >= len(initial_ids): initial_position = 0
                        else:
                            if roads_left == total_combinations / 2:
                                # Half of roads recently reached
                                initial_position = 0
                                pass
                            else:
                                initial_position -= 1
                                if initial_position < 0: initial_position = len(initial_ids) - 1
                        
                    #print(initial_position)
                    option_to_take = decision.options[initial_ids[initial_position]]
                else:
                    option_to_take:Option = decision.get_option_to_take(left_priority)

                #print(decision.name, option_to_take)
                if currentRoad.option_is_compatible(option_to_take):
                    left_priority = not left_priority
                    currentRoad.take_option(option_to_take)
                    option_to_take.times -= 1

        roads_left -= 1
        final_roads.append(currentRoad)
        currentRoad = ActionChain(points=novel_points)

        if roads_left == total_combinations / 2: left_priority = False


    print('Total combinations:', len(final_roads))
    u = GetSortedActionChain(final_roads)
    print(len(u))
    #for r  oad in GetSortedActionChain(final_roads):
        #print(road.summary(0))
    '''
        
        
    '''
    for decision in all_decisions:
        if decision.type == 'D':
            print(decision.name, decision.times)
            for option in decision.options:
                print(option, option.times)
    '''

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


def InitDecisionTree():
    for decision in all_decisions:
        if decision.type == 'D':
            decision.times = total_combinations
            times_per_option = int(total_combinations / len(decision.options))
            for option in decision.options:
                option.times = times_per_option


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