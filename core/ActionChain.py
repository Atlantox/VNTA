from core.Decision import Decision

class ActionChain:
    def __init__(self, decisions:list[Decision], points:list|dict):
        self.decisionChain = decisions
        self.idList = [d.id for d in self.decisionChain]

        if type(points) == list:
            self.points = {p:0 for p in points}
        elif type(points) == dict:
            self.points = points
        
        self.finished = None

    def __str__(self):
        return self.summary(0)

    def summary(self, detailLevel:int = 0):
        ''' Recieve a number between 0 and 3, while larger the number more info is displayed '''
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
                #  Return id, name, option and comment of each decision taked and the novel points evolution
                result = ''
                keys = list(self.points.keys())
                points_evolution = {k:0 for k in keys}
                header = 'Id | Name | Option | Comment | Point Evolution\n'
                result += f'Initial points: {points_evolution} \n'
                result += header
                result += ('#' * len(header)) + '\n'
                for decision in self.decisionChain:
                    for i in range(0,len(decision.points)):
                        if decision.points[i] is None: continue

                        points_evolution[keys[i]] += decision.points[i]

                    result += f'{decision.id}- {decision.name} ||| {decision.option} ||| {decision.comment} ||| {points_evolution}\n'
            elif detailLevel == 3:
                #  Return all information of each decision and the novel points evolution
                pass
            

        return result
    
    def get_decision_sequency(self):
        result = '*-'
        for d in self.decisionChain:
            result += str(d.id) + '-'
        if self.finished is not None: result += '* '
        result += f' {self.finished}'
        
        return result

    def get_str_points(self):
        points = '|  '
        for k,v in self.points.items():
            points += f'{k}:{v}  '
        return points

    def copy(self):
        return ActionChain(decisions=self.decisionChain.copy(), points=self.points)
    
    def take_decision(self, decision, change_points = True):
        self.decisionChain.append(decision)

        if change_points:
            self.change_points(decision)

        self.idList.append(decision.id)
        #print(self, 'Decision Taked:', decision.id)
        return self
    
    def change_points(self, decision):
        i = 0
        new_points = self.points.copy()
        if decision.points is not None:
            for k, v in new_points.items():
                if decision.points[i] is not None:
                    new_points[k] += decision.points[i]
                i += 1
        
        self.points = new_points
        return self
    
    def get_points_as_list(self):
        return [v for k,v in self.points.items()]
    
    def decision_is_compatible(self, decision:Decision):
        ''' Return True if the passed decision are valid to take, otherwhise return False '''
        if self.finished is not None:
            #  Finished ActionChains can't take more decisions
            return False

        if decision.dependency is not None and decision.dependency not in self.idList:
            #  If the decision depends of an previous decision that wasn't taked
            #  the ActionChain can't take that decision
            return False

        return True


    def finish(self, ending:str = 'Finished'):
        self.finished = ending
        lastDecision =self.decisionChain[-1]
        self.end = lastDecision.comment if lastDecision.comment else lastDecision.name
