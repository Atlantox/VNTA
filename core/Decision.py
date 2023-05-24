class Decision:
    '''
    A Decision is a fork in a visual novel's history, generally the player
    will select an option and take it.
    
    Many Decisions can have future consecuences, that consecuence
    "depends" of the original decision.

    Visual novels are common to have "points" like friendship or
    statistics like strength, speed, etc.

    Usually Decisions taked by the player can affect him statistics.

    Many Decisions can be "conditionals", these happens if the
    player have enough "points" or not.       
    '''
    def __init__(self, id, type, name, option, dependencies, points):
        self.id = id  # Unique identifier
        self.type = type  # [D]ecision, [C]onsecuence, [E]nding, [I]f
        self.name = name  # Name of the decision
        self.option = option  # Possible option that player can take
        self.dependencies = dependencies  # List of the previous decision's id that needs to be taked to take current decision
        self.points = points  # List of points, can be use to compare or add or delete points

    def __str__(self):
        return self.summary()
    
    def summary(self, deep_level:int=0, novel_points:list[str]=[]):
        ''' Between more big the deep_level, more details are displayed, by default 0 and max 2 '''
        if deep_level == 0:  # Display id and name
            return f'{self.id} || {self.name}'  
        if deep_level == 1:  # Display id, name, option and points
            points = self.get_points_as_str(novel_points)
            return f'{self.id} || {self.name} ||| {self.option} ||| {points}'
        if deep_level == 2:  # Display id, type, name, option, dependencies and points
            points = self.get_points_as_str(novel_points)
            return f'{self.id} || {self.type} || {self.name} ||| {self.option} ||| {self.dependencies} ||| {points}'
        
    
    def get_points_as_str(self, novel_points:list[str]):
        result = ''
        if novel_points == []:
            return self.points
        else:
            for i in range(len(novel_points)):
                result += f'{novel_points[i]}:  ({self.points[i]}) ||| '

        return result