import re
keywords = {'begin', 'end', 'if', 'then', 'elif', 'else', 'for', 'in', 'range', 'do'}
operators = {'+', '-', '*', '/', '='}
delimiters = {'(', ')', ','} 

def token_type(token):
    if token in keywords:
        return 'KEYWORD'
    elif token in operators:
        return 'OPERATOR'
    elif token.isdigit():
        return 'NUMBER'
    elif re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', token):  
        return 'IDENTIFIER'
    elif token in delimiters:
        return 'DELIMITER'
    else:
        return 'UNKNOWN'

def tokens_split(code):
    tokens = []
    cur_token = ""
    i = 0
    while i < len(code):
        char = code[i]        
        if char.isspace():
            if char == '\n':  
                i += 1
                continue
            else:
                if cur_token:
                    tokens.append((cur_token, token_type(cur_token)))
                    cur_token = ""
                i += 1
                continue
        
        if char in operators or char in delimiters:
            if cur_token:
                tokens.append((cur_token, token_type(cur_token)))
                cur_token = ""
            tokens.append((char, token_type(char)))
            i += 1
            continue
        
        if char.isalnum() or char == '_':cur_token += char
        else:
            if cur_token:
                tokens.append((cur_token, token_type(cur_token)))
                cur_token = ""
        i += 1
    
    if cur_token:
        tokens.append((cur_token, token_type(cur_token)))
    return tokens

code = """
begin
    x = 7 + 4 * 3
    y = 10 - 6 / 3
    begin
        if x < y then
            z = x + y
        elif x == y then
            z = x * y
        else
            z = x - y
        end
    end

    begin
        for i in range(1, 10) do
            x = x + i
            begin
                for j in range(1, 10) do
                    y = y * j
                end
            end
        end
    end
"""

tokens = tokens_split(code)
print(f"token\t \ttoken_type\n")

for token, token_type in tokens:
    print(f"{(token)}\t:\t{token_type}")
