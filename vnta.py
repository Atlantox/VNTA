from ActionChain import ActionChain
from Decision import Decision


# id, type, name, option, comment, friendship, qualification
# 22;D;qué hacer?;nada;;0;0
# 23;D;¿qué hacer?;atacar;;0;1

# 48;C;Estás a punto de caerte;22;No hiciste nada;0;0
# 49;C;Estás a punto de caerte;23;Atacaste;0;0

# 55;I;El instructor habla de su pasado;>=;Ficha del instructor desbloqueado;;6
# 56;I;Situación rara;>=,<;;4;6

# 102;GE;El prota vive feliz con la chica;>=;Final bueno;8;
# 103;BE;El prota se suicida;<;Final malo;8;

def run():
    original_points = {'amistad':0, 'calificación':0}
    endings = {}

    all_decisions = ReadDecisions()

    all_ways = []
    crt_dec = 0  # Current decision

    while crt_dec < len(all_decisions):
        currentDecision =  all_decisions[crt_dec]

        if currentDecision.type.upper() == 'D':  # Decision
            i = 1
            related_decisions = [currentDecision]
            while currentDecision.name == all_decisions[crt_dec + i].name:
                related_decisions.append(all_decisions[crt_dec + i])
                i += 1
                if crt_dec + i >= len(all_decisions): break

            crt_dec += i - 1
            i = 0


            if all_ways == []:
                for r in related_decisions:                    
                    to_add = ActionChain([r], original_points).change_points(r)
                    all_ways.append(to_add)

            else:
                for i in range(len(all_ways)):
                    original_way = all_ways[i].copy()
                    
                    if all_ways[i].finished:
                        continue

                    first = True
                    for r in related_decisions:
                        if first:
                            all_ways[i].take_decision(r)
                            first = False
                        else:
                            all_ways.append(original_way.copy().take_decision(r))


        elif currentDecision.type == 'C':  # Consecuence
            if all_ways == []:
                print(f'Consecuences needs a anterior decision in {currentDecision}')
            else:
                for way in all_ways:
                    if way.finished:
                        continue

                    if int(currentDecision.option) in way.idList:
                        way.take_decision(currentDecision)

        elif currentDecision.type == 'I':   # If condition
            for way in all_ways:
                if way.finished:
                    continue

                CheckCondition(way, currentDecision)

        # 102;ED-good;El prota vive feliz con la chica;>=;Final bueno;8;
        # 103;ED-end;El prota se suicida;<;Final malo;8;
        elif 'ED-' in currentDecision.type:  # Good ending
            for way in all_ways:
                if way.finished:
                    continue
                
                if CheckCondition(way, currentDecision):
                    way.finish()

                    endingType = currentDecision.type.split('-')[1]
                    try:
                        endings[endingType] += 1
                    except KeyError:
                        endings[endingType] = 1
                        

        else:
            print(f'{currentDecision.id} decision has wrong type: {currentDecision.type}')

        crt_dec += 1

    print('')
    #for way in all_ways:
        #print(way, '····', way.points)

    print('Total ways:', len(all_ways))
    #print('Endings:', endings)

    totals = f'\nTotal endings:\n'
    for key, value in endings.items():
        percent = (value * 100) / len(all_ways)
        totals += f'{key}: {value} -> {percent}% -> {percent / 100} \n'

    print(totals)

def ReadDecisions():
    decisions = []
    with open('decisions.csv') as f:
        lines = f.readlines()
        f.close()
    
    for line in lines:
        print(line)

    decisions = [
        Decision(1, 'D', '¿qué hacer?', 'nada', '', [1,None]),
        Decision(2, 'D', '¿qué hacer?', 'atacar', '', [None,1]),
        Decision(3, 'D', '¿a quien le das el pescado?', 'A Kat', '', None),
        Decision(4, 'D', '¿a quien le das el pescado?', "a Liz'Amar", '', [4,None]),
        Decision(5, 'D', "Con Liz'Amar solos en la habitación de Berto", "Pasar el rato con ella", 'follan', [2,-2]),
        #Decision(20, 'ED-bad', "Expulsado por inepto", "<", 'Final malo', [None, -1]),
        Decision(6, 'D', "Con Liz'Amar solos en la habitación de Berto", "Salir a entrenar", 'No follan', [-2,2]),
        Decision(7, 'D', "Mark'Zarog te pide que lo ayudes con Ámber", "Ayudarlo", '', None),
        Decision(8, 'D', "Mark'Zarog te pide que lo ayudes con Ámber", "Negarte", '', [None,1]),
        Decision(9, 'D', "¿a quién invitar a salir?", 'Ámber', '', None),
        Decision(10, 'D', "¿a quién invitar a salir?", 'Kat', '', [2, None]),
        Decision(11, 'D', "¿a quién invitar a salir?", 'Instructor', '', [None, 2]),
        Decision(12, 'D', "¿a quién invitar a salir?", "Mark'Zarog", '', None),
        Decision(13, 'C', "Le diste el pescado a Kat", "3", 'Te follas a Kat', None),
        Decision(14, 'C', "Le diste el pescado a Liz'Amar", "4", 'Follan', None),
        Decision(15, 'I', "El jefe te interrumpe", ">=", 'Ficha del jefe desbloqueada', [None, 3]),
        Decision(16, 'I', "El jefe te interrumpe", "<", 'Sales a entrenar', [None, 3]),
        Decision(17, 'ED-good', "Te quedas con la chica", ">=", 'Final bueno', [4, None]),
        Decision(18, 'ED-neutral', "La chica te rechaza pero siguen siendo amigos", "=", 'Final neutral', [3, None]),
        Decision(19, 'ED-bad', "El prota se suicida", "<", 'Final malo', [3, None])
        ]
    
    return decisions


def CheckCondition(way:ActionChain, decision:Decision):
    i = 0
    decision_taked = False
    for operator in decision.option.split(','):
        while decision.points[i] is None:
            i += 1
        
        if ConditionIsRight(way.get_points_as_list()[i], operator, decision.points[i]):
            way.take_decision(decision, False)
            decision_taked = True
        i += 1

    return decision_taked


def ConditionIsRight(left, operator, right):
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

if __name__ == '__main__':
    run()