import re
import tkinter as tk
from tkinter import filedialog, scrolledtext

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
    elif re.match(r'[a-zA-Z_][a-zA_0-9]*', token):
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
        
        if char.isalnum() or char == '_':
            cur_token += char
        else:
            if cur_token:
                tokens.append((cur_token, token_type(cur_token)))
                cur_token = ""
        i += 1
    
    if cur_token:
        tokens.append((cur_token, token_type(cur_token)))
    return tokens

def process_file():
    filepath = filedialog.askopenfilename(title="Open Code File", filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as file:
            code = file.read()
        tokens = tokens_split(code)
        
        output_box.delete('1.0', tk.END)
        
        for token, token_type in tokens:
            output_box.insert(tk.END, f"{token:^40}{token_type:^40}\n", 'content')

# root = tk.Tk()
# root.title("Token Analyzer")
# root.geometry("1000x800")
# root.configure(bg="#f4f4f4")

# root.resizable(False, False)  

# title_label = tk.Label(root, text="Token Analyzer", font=("Arial", 24, "bold"), bg="#f4f4f4", fg="black")
# title_label.pack(pady=10)

# open_button = tk.Button(root, text="Open Code File", font=("Arial", 18), bg="#17ffff", fg="black", command=process_file)
# open_button.pack(pady=15)

# output_frame = tk.Frame(root, bg="#f4f4f4")
# output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# output_frame.grid_rowconfigure(0, weight=0)
# output_frame.grid_rowconfigure(1, weight=1)
# output_frame.grid_columnconfigure(0, weight=1)

# header_label = tk.Label(
#     output_frame,
#     text=f"{'Token':^40}{'Type':^40}",
#     font=("Courier New", 18, "bold"),
#     bg="#e8f0f8",
#     fg="#333"
# )
# header_label.grid(row=0, column=0, sticky="ew")

# output_box = scrolledtext.ScrolledText(
#     output_frame, wrap=tk.WORD, font=("Courier New", 16), bg="#ffffff", fg="#333"
# )
# output_box.grid(row=1, column=0, sticky="nsew")

# output_box.tag_config('content', font=("Courier New", 16), foreground="#555")

# root.mainloop()
