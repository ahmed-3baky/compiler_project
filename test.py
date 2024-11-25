def parse_equation(line: str):

    ops = {'+': 'ADDITION', '-': 'SUBTRACTION', '*': 'MULTIPLICATION', '/':'DIVISION'}
    
    if '+' in line and '-' in line:

        ind_mul =  line.rindex('+')
        ind_div = line.rindex('-')
        priority = max(ind_mul, ind_div)

    elif '+' in line:

        priority = line.rindex('+')

    elif '-' in line:

        priority = line.rindex('-')

    elif '*' in line and '/' in line:
        ind_mul =  line.rindex('*')
        ind_div = line.rindex('/')
        priority = max(ind_mul, ind_div)

    elif '*' in line:

        priority = line.rindex('*')

    elif '/' in line:

        priority = line.rindex('/')


    
    else:
        
        if line.strip().isalnum():
            return {'VARIABLE': [line.strip()]}
        return {'Literal': [line.strip()]}

    return {ops[line[priority]]: [parse_equation(line[:priority].strip()), parse_equation(line[priority + 1:].strip())]}

def parse_compare(condition):

    if '<=' in condition:
            return [{'EXPRESSION': [parse_equation(condition[:condition.index('<=')].strip())]}, {'OPERATOR': ['<=']}, {'EXPRESSION': [parse_equation(condition[condition.index('<=')+2:].strip())]}]
print(parse_compare('x + 6 <= y + 8'))