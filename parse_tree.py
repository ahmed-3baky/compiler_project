from tockenizer import tokens_split
import graphviz
import random
from queue import Queue

def get_tokens():

    with open('code.txt', 'r') as file:
        code = file.read()
    tokens = tokens_split(code)

    tokens_dic = {}
    for key, state in tokens:
        tokens_dic[key] = state

    return tokens_dic

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
        if line.strip().isnumeric():
            return {'Literal': [line.strip()]}
        return {'VARIABLE': [line.strip()]}

    return {ops[line[priority]]: [parse_equation(line[:priority].strip()), parse_equation(line[priority + 1:].strip())]}

def parse_compare(condition):

    if '<=' in condition:
        return [{'EXPRESSION': [parse_equation(condition[:condition.index('<=')].strip())]}, {'OPERATOR': ['<=']}, {'EXPRESSION': [parse_equation(condition[condition.index('<=')+2:].strip())]}]
    elif '>=' in condition:
        return [{'EXPRESSION': [parse_equation(condition[:condition.index('>=')].strip())]}, {'OPERATOR': ['>=']}, {'EXPRESSION': [parse_equation(condition[condition.index('>=')+2:].strip())]}]
    elif '<' in condition:
        return [{'EXPRESSION': [parse_equation(condition[:condition.index('<')].strip())]}, {'OPERATOR': ['<']}, {'EXPRESSION': [parse_equation(condition[condition.index('<')+1:].strip())]}]
    elif '>' in condition:
        return [{'EXPRESSION': [parse_equation(condition[:condition.index('>')].strip())]}, {'OPERATOR': ['>']}, {'EXPRESSION': [parse_equation(condition[condition.index('>')+1:].strip())]}]
    elif '==' in condition:
        return [{'EXPRESSION': [parse_equation(condition[:condition.index('==')].strip())]}, {'OPERATOR': ['==']}, {'EXPRESSION': [parse_equation(condition[condition.index('==')+2:].strip())]}]
    elif '!=' in condition:
        return [{'EXPRESSION': [parse_equation(condition[:condition.index('!=')].strip())]}, {'OPERATOR': ['!=']}, {'EXPRESSION': [parse_equation(condition[condition.index('!=')+2:].strip())]}]
                        
    
def make_parse_tree():

    global code_lines
    
    tree = {'program': []}

    with open('code2.txt', 'r') as file:
        code_lines = file.readlines()
    
    stack = []
    then = None
    for line in code_lines:

        if line.strip() == 'begin':
            stack.append({})
            stack[-1]['block'] = []
        
        elif '=' in line.strip() and '==' not in line.strip():
            assign = {'ASSIGNMENT': []}
            assign['ASSIGNMENT'].extend([{'VARIABLE': [line[:line.index('=')].strip()]}, {'EXPRESSION': [parse_equation(line[line.index('=') + 1:].strip())]}])
            if stack[-1]['block'] and 'If-Else' in stack[-1]['block'][0]:
                if 'THEN' in stack[-1]['block'][0]['If-Else'][-1]:
                    stack[-1]['block'][0]['If-Else'][-1]['THEN'].append(assign)
                else:
                    if 'ELSE' in stack[-1]['block'][0]['If-Else'][-1]:
                        stack[-1]['block'][0]['If-Else'][-1]['ELSE'][-1]['THEN'].append(assign)
                    else:
                        stack[-1]['block'][0]['If-Else'][-1]['ELIF'][-1]['THEN'].append(assign)
            else:
                stack[-1]['block'].append(assign)

        elif ' if ' in line:
            ifelse = {'If-Else': []}
            condition = line[line.index(' if ')+4: line.index(' then')].strip()
            ifelse['If-Else'].append({'CONDITION': parse_compare(condition)})
            ifelse['If-Else'].append({'THEN': []})
            stack[-1]['block'].append(ifelse)
        
        elif ' elif ' in line:
            ifelse = {'ELIF': []}
            condition = line[line.index(' elif ')+6: line.index(' then')].strip()
            ifelse['ELIF'].append({'CONDITION': parse_compare(condition)})
            ifelse['ELIF'].append({'THEN': []})     
            stack[-1]['block'][0]['If-Else'].append(ifelse)        

        elif ' else' in line:

            ifelse = {'ELSE': []}
            condition = line[line.index(' else')+6:].strip()
            ifelse['ELSE'].append({'THEN': []})     
            stack[-1]['block'][0]['If-Else'].append(ifelse)     

        elif line.strip() == 'end':
            if len(stack) > 1:
                block = stack.pop()
                stack[-1]['block'].append(block)
            else:
                tree['program'].append(stack.pop())

    return tree

def get_rand_str():
    strs = 'abcdefghijklmnobqrstuvwxyzABCDEFGHIJKLMNOBQRSTUVWXYZ0123456789!@#$%^&*()_+'
    node = random.sample(strs, 30)
    return ''.join(node)

def draw_tree(node_id, childs):

    for child in childs:

        if type(child) == str:
            new_node_id = get_rand_str()
            dot.node(new_node_id, child)
            dot.edge(node_id, new_node_id)
            continue   
        
        for key in child:
            new_node_id = get_rand_str()
            dot.node(new_node_id, key)
            dot.edge(node_id, new_node_id)
            draw_tree(new_node_id, child[key])

dot = graphviz.Digraph(name='parse tree', format='png')
node_id = get_rand_str()
dot.node(node_id, 'program')


tree = make_parse_tree()
print(tree)

draw_tree(node_id, tree['program'])

dot.render('parse_tree_image', view=True)