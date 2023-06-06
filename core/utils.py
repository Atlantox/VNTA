from openpyxl import load_workbook

from core.ActionChain import ActionChain
from core.Decision import Decision, Option

def GetFileNameAndFormat(path:str):
    ''' Get a file path and returns the file name without format, and the file format '''
    fileFullName = path.split('/')[-1]  # File name with format
    splits = fileFullName.split('.')
    fileFormat = '.' + splits[-1]

    fileName = ''
    for split in splits[:-1]:
        fileName += split
    
    return fileName, fileFormat


def ReadDecisions(filePath:str, fileFormat:str):
    ''' Return all decisions in the specified .csv or excel file and the novel points '''
    decisions = []
    if fileFormat == '.xlsx': # Excel file
        decisions, novel_points, endings = LoadDecisionsFromExcel(filePath)        
    elif fileFormat == '.csv':  # CSV file
        decisions, novel_points, endings = LoadDecisionsFromCSV(filePath)
        
    return decisions, novel_points, endings


def LoadDecisionsFromExcel(filePath:str):
    '''
    Return the Decisions list and novel points of target Excel file
    IMPORTANT: the decisions must stay in a sheet named 'decisions'
    '''
    decisions = []
    endings = {}
    excel = load_workbook(filename=filePath, read_only=True)
    sheet = excel['decisions']
    rows = sheet.iter_rows()
    all_rows = [r for r in rows if str(r[0].value) != 'None']

    i = 0
    while(i < len(all_rows)):
        row = all_rows[i]
        if i == 0:
            # Getting the novels points names
            novel_points = [str(c.value).strip() for c in row[5:] if str(c.value).strip() != '' and c.value is not None]
    
        else:
            decision_name = str(row[2].value)
            related_rows = [row]
            relatedCounter = 1
            searching = True
            while(searching):
                try:
                    next_row = all_rows[i + relatedCounter]
                    # If the name is None and the id cell is not empty, then is a decision with more than one option
                    #print(str(next_row[0].value) == 'None')

                    if str(next_row[2].value) == 'None':
                        related_rows.append(next_row)
                        relatedCounter += 1
                    else:
                        searching = False
                except:
                    searching = False
            
            i += relatedCounter - 1
            options = []
            for related in related_rows:
                #  Getting the first 5 fields (id, type, name, option, dependency)
                id, dtype, name, option, dependencies = [str(c.value) for c in related[:5]]
                if 'E-' == dtype[0:2]:
                    ending_name = dtype[2:]
                    if ending_name not in endings: endings[ending_name] = 0

                points = [str(c.value) for c in related[5:5 + len(novel_points)]]
                points, dependencies = GetPointsAndDependencies(points, dependencies)

                if dtype == 'I' or 'E-' == dtype[0:2]:
                    if ',' in option: option = [n.strip() for n in option.split(',')]

                options.append(Option(
                    id=id, 
                    name=option,
                    dependencies=dependencies,
                    points=points
                ))

            decisions.append(Decision(
                id=id,
                type=dtype,
                name=decision_name,
                options=options,
            ))

        i+=1

    return decisions, novel_points, endings


def GetPointsAndDependencies(points:list[str], dependencies:str):
    local_points = []
    local_dependencies = []
    for point in points:
        #  Converting the points in to useful values
        if (point != 'None' or point is not None) and point != '': 
            local_points.append(int(point))
        else: local_points.append(None)            

    if dependencies != 'None':
        # If the decision has dependency, convert the string into a list
        local_dependencies = [s.strip() for s in dependencies.split(',') if s != ''] 
    else: local_dependencies = None

    return local_points, local_dependencies


def LoadDecisionsFromCSV(filePath:str):
    ''' Return a list of Decisions and novel_points of target CSV file '''
    decisions = []
    endings = {}
    with open(filePath, 'r', encoding='utf-8') as f: #  Open the CSV file
        lines = f.readlines()
        f.close()
    
    # Getting the novel points names
    novel_points = [l.strip() for l in lines[0].split(';')[5:]]

    crt_id = 1
    rows = len(lines[1:])
    related_lines = []

    while crt_id < rows:
        current_line = lines[crt_id].split(';')
        related_lines = [current_line]
        
        count = 1
        while True:
            try:
                new_line = lines[crt_id + count].split(';')
            except:
                break
            
            if [new_line[1], new_line[2]] == [current_line[1], current_line[2]]: # The line has the same name and type
                related_lines.append(new_line)
                count += 1
            else:
                break
        crt_id += count - 1

        options = []
        for row in related_lines:
            id = row[0]
            dtype = row[1]
            decision_name = row[2]
            option = row[3]
            dependencies = row[4]

            if 'E-' == dtype[0:2]:
                ending_name = dtype[2:]
                if ending_name not in endings: endings[ending_name] = 0

            points = [p.strip() for p in row[5:5 + len(novel_points)]]
            points, dependencies = GetPointsAndDependencies(points, dependencies)

            options.append(Option(
                id = id,
                name = option,
                points = points,
                dependencies = dependencies
            ))

        
        decisions.append(Decision(
            id=id,
            type=dtype,
            name=decision_name,
            options=options,
        ))

        crt_id+=1

    return decisions, novel_points, endings


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
    ''' Return True if (left operator right), otherwise return False '''
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
    ''' Gets a list of ActionChain and returns it sorted by IdList '''
    decisions = dict()
    sortedDecisions = []
    for way in ways:
        if way.get_decision_sequency() in decisions.keys(): print(way, 'repetido')
        decisions[way.get_decision_sequency()] = way
    print('luego de guardar', len(decisions))
    keys = list(decisions.keys())
    print('antes de ordenar', len(keys))
    keys.sort()
    print('despues de ordenar', len(keys))
    for d in keys:
        sortedDecisions.append(decisions[d])

    return sortedDecisions


def GetEndingStatistics(endings:dict, roads:int):
    ''' Return a dict with statistics of endings given '''
    result = {}
    for key, value in endings.items():
        percent = round((value * 100) / roads, 2)
        to_add = {
            'count': value,
            'percent': f'{percent:.2f}',
            'index': f'{(percent / 100):.2f}'
        }
        result[key] = to_add

    return result