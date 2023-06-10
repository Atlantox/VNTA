import os
import pickle

from tkinter import messagebox

from core.utils import *


AVAILABLE_FORMATS = ['.csv', '.xlsx']
filePath = ''
fileName = ''
fileFormat = ''
progress_info = None
window_frame = None
full_mode = False
total_combinations = 0
all_ways:list[ActionChain] = []  # The list of all ActionChain
all_decisions:list[Decision] = []
novel_points:list[str] = []  # The novel points names
endings = {}  # Ending statistics


def StartDecisionsTree(path, lite_mode, progress_label, frame):
    ''' Reset all the global variables and Create or load the decision tree if exists '''
    global all_decisions, novel_points, fileName, filePath, fileFormat, all_ways, endings, full_mode, progress_info, window_frame, total_combinations
    total_combinations = 0
    progress_info = progress_label
    window_frame = frame
    full_mode = not lite_mode
    all_ways, all_decisions, novel_points = [], [], [] # Cleaning global variables
    endings = {}
    filePath = path
    fileName, fileFormat = GetFileNameAndFormat(filePath)

    if fileFormat in AVAILABLE_FORMATS:
        all_decisions, novel_points, endings = ReadDecisions(filePath, fileFormat)
        CreateDecisionsTree()
    elif fileFormat == '.vnta':
        LoadDecisionsTree(path)  

    return all_decisions, all_ways, endings, novel_points

def explore_decision_tree(decisions:list[Decision], current_path:ActionChain, all_paths:list):
    ''' 
    A recursive function that explores all possible ways
    '''
    if current_path == []:
        # If the current path is empty, then create one
        current_path = ActionChain(points=novel_points)

    if not decisions:
        # If not decisions left, then the ActionChain ends
        global total_combinations
        total_combinations += 1 # The ways finished
        try:
            progress_info.config(text=total_combinations)
            # We set the text of the progress info in the window to give feedback to user
        except:
            # If the user close the window, the program will stop
            exit()

        # Necesary for update the progress info text
        window_frame.update()

        if full_mode:
            # If the user is un full mode, then save the road
            AddNewRoad(current_path, all_paths, True)
        return  # The recursivity ends

    current_decision = decisions[0] # The first Decisions
    remaining_decisions = decisions[1:] # The rest of Decisions
    original_path = current_path.copy() # We create a copy to prevent duplicates

    for option in current_decision.options:
        # For each option, if the option is compatible, take it
        if original_path.option_is_compatible(option, current_decision.type):
            if 'E-' == current_decision.type[0:2]:
                # If the option is a Ending, then add the statistic to the endings global variable
                endingType = current_decision.type[2:]
                global endings
                endings[endingType] += 1
                # We call the self function but passing a empty list in the decisions parameter
                # This will force the end of the road
                explore_decision_tree([], original_path.copy().take_option(option, current_decision.type), all_paths)
            else:
                # If is not a ending, then just take the Decision and continue with the rest of decision
                explore_decision_tree(remaining_decisions, original_path.copy().take_option(option, current_decision.type), all_paths)
        else:
            # The Decision is not compatible, then continues with the rest of Decisions
            explore_decision_tree(remaining_decisions, original_path, all_paths)


def AddNewRoad(road:ActionChain, all_paths:list, force_save = False):
    all_paths.append(road)  # Saving the current road
    if len(all_paths) == 1000000 or force_save:
        '''
        If the list of roads reach one million of roads
        append that million of roads in a .vnta file to clean RAM
        WARNING: ONE MILLION OF ROADS ARE NEAR OF 200MB SO BECAREFUL WITH THAT
        '''
        with open(f'{fileName}.vnta', 'ab') as f:
            for path in all_paths:
                pickle.dump(path, f)
            all_paths.clear()

def CreateDecisionsTree():
    ''' Each Decision branches the start point creating a tree of Decisions '''
    global all_ways
    if os.path.exists(f'{fileName}.vnta') and full_mode:
        # we delete the file if the user is in full mode
        os.remove(f'{fileName}.vnta')

    all_ways = []
    explore_decision_tree(all_decisions, [], all_ways)  # Exploring ALL posible paths

    if full_mode:
        #  Save important info in the last element of the file
        to_save = {
            'all_decisions': all_decisions,
            'novel_points': novel_points,
            'endings': endings
        }

        with open(f'{fileName}.vnta', 'ab') as f:
            # Saving the info in the .vnta file
            pickle.dump(to_save, f)

        # Now the load ALL paths from that file
        # REMEMBER: BE CAREFUL WITH YOU DISK SPACE
        LoadDecisionsTree(f'{fileName}.vnta')
        messagebox.showinfo('Success', 'Decision tree successfully created and saved as: ' + f'{fileName}.vnta')
    else:
        # If the user is in lite mode then just shows the endings statistics
        to_add = f'Caminos posibles: {total_combinations}\nEndings:'

        statistics = GetEndingStatistics(endings, total_combinations)
        for key, value in statistics.items():
            to_add += f"\n   {key}:\n      Cantidad: {value['count']}\n      Porcentaje: {value['percent']}%\n      Índice: {value['index']}\n"

        # We save the results in a .txt
        with open(f'{fileName}.txt', 'w', encoding='utf-8') as f:
            f.write(to_add)       
        messagebox.showinfo('Success', 'Ending statistics successfully placed in: ' + f'{fileName}.txt')


def LoadDecisionsTree(path):
    '''
    If a .vnta file is given, all data is loaded from that file
    This function is usefull when you have a really really big decision tree
    But a really really big decision tree means a really big space in disk
    REMEMBER: BE CAREFUL WITH YOUR DISK SPACE
    '''
    elements = []
    with open (path, 'rb') as f:
        while True:
            try:
                element = pickle.load(f)
                elements.append(element)
            except:
                break

    data = elements[-1]
    #  Cleaning the global variables
    all_ways.clear()
    novel_points.clear()
    endings.clear()
    all_decisions.clear()
    # Filling the global variables
    for w in elements[0:-1]: all_ways.append(w)
    for p in data['novel_points']: novel_points.append(p)
    for e, v in data['endings'].items(): endings[e] = v
    for d in data['all_decisions']: all_decisions.append(d)

    messagebox.showinfo('Success', 'Decision tree successfully loaded')


def GetDecisionsBySearch(search_type:str, search:str = ''):
    '''
    Return a list of the Decisions depending of a search
    search can be by 'id', 'name', 'option', 'dependency' and 'points'
    do a '*' search to get all Decisions
    '''
    if search == '*':
        return all_decisions

    results = []
    items = [v.strip().lower() for v in search.split(',') if v != '']

    if search_type == 'id':
        for d in all_decisions:
            for option in d.options:
                if option.id.lower() in items: results.append(d)                

    elif search_type == 'name':
        for d in all_decisions:
            for name in items:
                if name in d.name.lower():
                    results.append(d)
                    break
                
    elif search_type == 'option':
        for d in all_decisions:
            for option in d.options:
                if option.name is not None and option.name.lower() in items:
                        results.append(d)
                        break

    elif search_type == 'dependency':
        for d in all_decisions:
            for option in d.options:
                # If the option have dependencies and these dependencies match with the items
                if option.dependencies is not None and (set(option.dependencies) & set(items)):
                    results.append(d)
                    break

    elif search_type == 'points':
        indexes = [id for id, value in enumerate(novel_points) if value in items]

        if len(novel_points) != 0:
            for d in all_decisions:
                found = False
                for option in d.options:
                    found = any(index in indexes for index, _ in enumerate(option.points) if _ is not None)
                    if found: break

                if found: results.append(d)

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