from core.Decision import Decision

class ActionChain:
    '''
    An ActionChain is a sucession of Decisions like a chain
    each ActionChain represent a possible road that a player
    can play.

    A list of ActionChain with all possible roads of a visual novel 
    is named Decision Tree

    A Decision Tree allows to know how many balanced is a visual novel
    
    Knowing how many balance is your visual novel, allows you to
    create a difficult or easy game based in bad ending and good ending
    '''
    def __init__(self, decisions:list[Decision], points:list|dict):
        self.decisionChain = decisions  # A ordered list of decisions already taken
        self.idList = [d.id for d in self.decisionChain]  # A list of the ids of taken decisions

        if type(points) == list:
            self.points = {p:0 for p in points}  # The points of the novel
        elif type(points) == dict:
            self.points = points
        
        self.finished = None  # None if the chain is not finished

    def __str__(self):
        return self.summary(0)

    def summary(self, detailLevel:int = 0):
        ''' Recieve a number between 0 and 2, while larger the number more info is displayed '''
        result = 'Empty'
        if self.decisionChain:
            if detailLevel == 0:
                #  Return the sequence of ids of all decisions
                result = self.get_decision_sequency()

            elif detailLevel == 1:
                #  Return the sequence of ids of all decisions and the total novel points
                result = self.get_decision_sequency()                
                result += self.get_str_points()

            elif detailLevel == 2:
                #  Return id, name, option and dependencies of each decision taken and the novel points evolution
                result = ''
                keys = list(self.points.keys())
                points_evolution = {k:0 for k in keys}
                header = 'Id | Name | Option | Dependencies | Point Evolution\n'
                result += f'Initial points: {points_evolution} \n'
                result += header
                result += ('#' * len(header)) + '\n'
                for decision in self.decisionChain:
                    for i in range(0,len(decision.points)):
                        if decision.points[i] is None: continue

                        points_evolution[keys[i]] += decision.points[i]

                    result += f'{decision.id}- {decision.name} ||| {decision.option} ||| {decision.dependencies} ||| {points_evolution}\n'            

        return result
    
    def get_decision_sequency(self):
        '''
        Return a string with a sequency of decisions's id taken
        example: *-1-3-5-8-11-15-
        '''
        result = '*-'
        for d in self.decisionChain:
            result += str(d.id) + '-'
        if self.finished is not None: 
            result += f' {self.finished}'
        else:
            result += result[:-1] + ' #-Unfinished-#'
        
        return result

    def get_str_points(self):
        '''
        Return a string with the current novel_points
        example: fiendship: (5), strength: (-1)
        '''
        points = '   |||      '
        for k,v in self.points.items():
            points += f'{k}: ({v})  '
        return points

    def copy(self):
        ''' Return a new equal ActionChain instance '''
        return ActionChain(decisions=self.decisionChain.copy(), points=self.points)
    
    def take_decision(self, decision, change_points = True):
        ''' Take a decision and add it to the decision chain '''
        self.decisionChain.append(decision)

        if change_points:
            self.change_points(decision)

        self.idList.append(decision.id)
        return self
    
    def change_points(self, decision):
        ''' Modify the points of the ActionChain depending of the decision given '''
        i = 0
        new_points = self.points.copy()
        if decision.points != [None] * len(decision.points):
            for k, v in new_points.items():
                if decision.points[i] is not None:
                    new_points[k] += decision.points[i]
                i += 1
        
        self.points = new_points
        return self
    
    def get_points_as_list(self):
        ''' Return the points dict values as a list '''
        #return [v for v in self.points.values()]
        return list(self.points.values())
    
    def decision_is_compatible(self, decision:Decision):
        ''' Return True if the passed decision are valid to take, otherwhise return False '''
        #if self.finished is not None:
            #  Finished ActionChains can't take more decisions
            #return False

        if decision.dependencies is not None:
            #  If the decision depends of an previous decision that wasn't taken
            #  the ActionChain can't take that decision
            for dependency in decision.dependencies:
                if dependency[0] == '-':  #  Negative dependency
                    if dependency[1:] in self.idList: return False
                else:
                    if dependency not in self.idList: return False

        return True

    def finish(self, ending:str = 'Finished'):
        ''' Mark the ActionChain as finished '''
        self.finished = ending
