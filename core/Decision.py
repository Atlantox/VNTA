# id, type, name, option, comment, friendship, qualification
# 22;D;qué hacer?;nada;;0;0
# 23;D;¿qué hacer?;atacar;;0;1

# 48;C;Estás a punto de caerte;22;No hiciste nada;0;0
# 49;C;Estás a punto de caerte;23;Atacaste;0;0

# 55;I;El instructor habla de su pasado;>=;Ficha del instructor desbloqueado;;6
# 56;I;Situación rara;>=,<;;4;6

# 102;GE;El prota vive feliz con la chica;>=;Final bueno;8;
# 103;BE;El prota se suicida;<;Final malo;8;

class Decision:
    def __init__(self, id, type, name, option, dependencies, comment, points):
        self.id = id
        self.type = type
        self.name = name
        self.option = option
        self.dependencies = dependencies
        self.comment = comment
        self.points = points

    def __str__(self):
        return self.summary()
    
    def summary(self, deep_level:int=0):
        if deep_level == 0:
            return f'{self.id} || {self.name}'
        if deep_level == 1:
            return f'{self.id} || {self.name} ||| {self.option} ||| {self.dependencies} ||| {self.points}'