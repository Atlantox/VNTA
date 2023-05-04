from Decision import Decision
# id, type, name, option, comment, friendship, qualification

class ActionChain:
    def __init__(self, decisions:list, points:list|dict):
        self.decisionChain = decisions
        self.idList = [d.id for d in self.decisionChain]

        if type(points) == list:
            self.points = {p:0 for p in points}
        elif type(points) == dict:
            self.points = points
        self.finished = False

    def __str__(self):
        if self.decisionChain:
            result = '*-'
            for d in self.decisionChain:
                result += str(d.id) + '-'
            if self.finished:
                result += '*'
            return result
        
        return 'Empty'

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
    
    def finish(self):
        self.finished = True
        lastDecision =self.decisionChain[-1]
        self.end = lastDecision.comment if lastDecision.comment else lastDecision.name
