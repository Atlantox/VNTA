class Option():
    '''
    An Option is a Option of a Decision that the player can take
    But an Option are too a situation or scene that trigger depending of a condition

    An Option has a type:
        'D' -> Decision: A Decision is a list of related Options that can be taked by the player
                       each Option of this type, will branch the visual novel's history,
                       to create a Decision of this type, they need to have the same name

        'C' -> Consecuence: A consecuence is a scene o situation that triggers if the player
                          has taken a previous decision or not

        'I' -> If conditional: A If conditional Option triggers only if the player meets certain 
                             a certaion conditions or conditions

        'E-' -> Ending: An ending is one possible end of the visual novel, that endings needs
                        a name, example: E-good, E-bad, the end needs a condition to be taked
    '''
    def __init__(self, id:str, name:str|list[str], dependencies:list, points:list):
        self.id = id
        self.name = name
        self.dependencies = dependencies
        self.points = points

    def __str__(self):
        return f'{self.name}'
    
    def get_points_as_str(self, novel_points:list[str]):
        ''' Get the points of the Decision in a friendly string '''
        result = ''
        if novel_points == []:
            return self.points
        else:
            for i in range(len(novel_points)):
                result += f'{novel_points[i]}:  ({self.points[i]}) ||| '

        return result

class Decision:
    '''
    A Decision can be two things:
    A group of related options that branches the visual novel's history
    A decision or situation that will happen or not

    But the most important is that a Decision is a wrapper of Options,
    the important thing are the options
    
    Many Decisions can have future consecuences, that consecuence
    "depends" of the original decision.

    Visual novels are common to have "points" like friendship or
    statistics like strength, speed, etc.

    Usually Decisions taked by the player can affect him statistics.

    Many Decisions can be "conditionals", these happens if the
    player have enough "points" or not.       
    '''
    def __init__(self, id:str, type:str, name:str, options:list[Option]):
        self.id = id  # Unique identifier
        self.type = type  # [D]ecision, [C]onsecuence, [E]nding, [I]f
        self.name = name  # Name of the decision
        self.options = options  # Possible option that player can take

    def __str__(self):
        return f'{self.id} || {self.name}'  