from core.Decision import Decision, Option

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
    def __init__(self, points:list|dict, idList:list = []):
        self.idList = idList if idList else []

        if type(points) == list:
            self.points = {p:0 for p in points}  # The points of the novel
        elif type(points) == dict:
            self.points = points
        
        self.finished = None  # None if the chain is not finished

    def __str__(self):
        return self.summary(0)

    def summary(self, detailLevel:int = 0):
        ''' Recieve a number between 0 and 1, while larger the number more info is displayed '''
        result = 'Empty'
        if self.idList != []:
            if detailLevel == 0:
                #  Return the sequence of ids of all decisions
                result = self.get_decision_sequency()

            elif detailLevel == 1:
                #  Return the sequence of ids of all decisions and the total novel points
                result = self.get_decision_sequency()                
                result += self.get_str_points()            

        return result
    
    def get_decision_sequency(self, only_ids = False):
        '''
        Return a string with a sequency of decisions's id taken
        example: *-1-3-5-8-11-15-
        '''
        result = '*-'
        for id in self.idList:
            result += id + '-'
        
        if not only_ids:
            if self.finished is not None: 
                result += f' {self.finished}'
            else:
                result += ' #-Unfinished-#'
        
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
        return ActionChain(points=self.points.copy(), idList=self.idList.copy())
    
    def take_option(self, option:Option, dtype:str, change_points = True):
        '''
        Take an option an add it to the idList of options taked
        If change_poitns = True, then the ACtionChain will modify
        the points
        If the option is a ending, then the ActionChain finish
        '''
        if 'E-' == dtype[0:2] or dtype == 'I':
            change_points = False

        if change_points:
            self.change_points(option)

        self.idList.append(option.id)
        if 'E-' == dtype[0:2]: self.finish(dtype[2:])
        return self
    
    def change_points(self, option:Option):
        ''' Modify the points of the ActionChain depending of the decision given '''
        i = 0
        new_points = self.points.copy()

        if option.points != [None] * len(option.points):
            for k, v in new_points.items():
                if option.points[i] is not None:
                    new_points[k] += option.points[i]
                i += 1
        
        self.points = new_points
        return self
    
    def get_points_as_list(self):
        ''' Return the points dict values as a list '''
        return list(self.points.values())
    
    def option_is_compatible(self, option:Option, dtype:str):
        ''' Return True if the passed decision are valid to take, otherwhise return False '''
        
        #  Finished ActionChains can't take more decisions
        if self.finished is not None: return False
        
        is_compatible = True
        if option.dependencies is not None:
            #  If the decision depends of an previous decision that wasn't taken
            #  the ActionChain can't take that decision
            for dependency in option.dependencies:
                if dependency[0] == '-':  #  Negative dependency
                    if dependency[1:] in self.idList: 
                        is_compatible = False
                        break
                else:  # Positive dependency
                    if dependency not in self.idList:
                        is_compatible = False
                        break

        if dtype == 'I' or 'E-' in dtype:
            # If the Decision is E- or I type, then ckeck if the current
            # meets the conditions
            for id, point in enumerate(self.points.keys()):
                if option.points[id] is not None:
                    if type(option.name) == list:
                        is_compatible = self.condition_is_right(self.points[point], option.name[id], option.points[id])
                    elif type(option.name) == str:
                        is_compatible = self.condition_is_right(self.points[point], option.name, option.points[id])
                    if not is_compatible: break

        return is_compatible

    def finish(self, ending:str = 'Finished'):
        ''' Mark the ActionChain as finished '''
        self.finished = ending

    def condition_is_right(self, left, operator, right):
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