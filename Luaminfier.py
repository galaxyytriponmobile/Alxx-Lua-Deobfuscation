import re
import os
import base64

# --- Beautifier Function ---
def beautify_code(code):
    indent_level = 0
    beautified_code = ''
    indent_keywords = {'function', 'if', 'else', 'elseif', 'for', 'while', 'do'}
    unindent_keywords = {'end', 'else', 'elseif'}
    lines = re.split(r'(\b(?:function|if|else|elseif|for|while|do|end)\b|\n|;)', code)

    for line in lines:
        stripped_line = line.strip()

        if stripped_line in unindent_keywords:
            indent_level -= 1

        if stripped_line:
            beautified_code += '    ' * indent_level + stripped_line + '\n'

        if stripped_line in indent_keywords:
            indent_level += 1

    return beautified_code.strip()

# --- Add New Line After Semicolons and Ensure New Lines ---
def add_newlines_after_semicolons(code):
    # Add a newline after each semicolon, but keep the semicolon
    code = re.sub(r';', ';\n', code)
    
    # Add newlines after closing brackets (), {}, or []
    code = re.sub(r'(\)|\}|\])', r'\1\n', code)

    # Ensure that lines after closing brackets start on a new line
    lines = code.splitlines()  # Split into individual lines
    
    # Ensure each line starts on a new line
    formatted_code = '\n'.join(line.strip() for line in lines if line.strip())  # Removing any extra spaces and blank lines
    return formatted_code

# --- Lua Parsing Functions ---
def parse_lua_code(code):
    variables = re.findall(r'local\s+([\w_]+)\s*=', code)
    functions = re.findall(r'function\s+([\w_]+)\s*\(', code)
    return variables, functions

def deobfuscate_variables(code, variables):
    deobf_map = {}
    counter = 1
    
    for var in variables:
        deobf_var = f'deobf_{counter}'
        deobf_map[var] = deobf_var
        counter += 1

    for var, deobf_var in deobf_map.items():
        code = re.sub(r'\b' + re.escape(var) + r'\b', deobf_var, code)

    return code

def deobfuscate_functions(code, functions):
    deobf_map = {}
    counter = 1

    for func in functions:
        deobf_func = f'deobf_func_{counter}'
        deobf_map[func] = deobf_func
        counter += 1

    for func, deobf_func in deobf_map.items():
        code = re.sub(r'\b' + re.escape(func) + r'\b', deobf_func, code)

    return code

def decode_strings(code):
    def decode_base64(match):
        encoded_str = match.group(1)
        try:
            decoded_bytes = base64.b64decode(encoded_str).decode('utf-8')
            return f'"{decoded_bytes}"'
        except Exception:
            return match.group(0)

    return re.sub(r'base64.decode\("([^"]+)"\)', decode_base64, code)

# --- Makeshift Decompiler with More Features ---
def makeshift_decompiler(code):
    # --- Function Simplification ---
    # Simplify function definitions with obfuscated arguments
    code = re.sub(r'function\s*\(.*?\)', 'function(...)', code)  # Simplify function to use variable arguments
    
    # --- Common Obfuscation Patterns ---
    # Reconstruct loops
    code = re.sub(r'for\s*([\w_]+)\s*=.*?do', r'for \1 = ... do', code)  # Simplify obfuscated loops
    
    # Simplify if conditions with complex logic
    code = re.sub(r'if\s*\(.*?\)\sthen', 'if condition then', code)  # Simplify complex conditions
    
    # --- String Manipulation Patterns ---
    # Detect and reverse common string obfuscation patterns
    # For example: string.char(65, 66, 67) -> "ABC"
    code = re.sub(r'string\.char\(([\d, ]+)\)', lambda match: ''.join(chr(int(x)) for x in match.group(1).split(',')), code)

    # --- Deobfuscate Tables ---
    # Decompile common table-based obfuscations (arrays of functions/strings)
    # For example: table = { [1] = "print('Hello')" } -> table = { "print('Hello')" }
    code = re.sub(r'\[(\d+)\]\s*=\s*', '', code)  # Simplify table access using numbers as keys
    
    # Detect and deobfuscate common function call patterns
    code = re.sub(r'\w+\(\s*function\s*\(.*?\)\s*', 'function(...) ', code)  # Simplify inline function calls
    
    # --- Math Obfuscation Simplifications ---
    # Decompile common math-based obfuscation (e.g., constant arithmetic)
    # For example: 10 + 5 -> 15
    code = re.sub(r'(\d+)\s*\+\s*(\d+)', lambda match: str(int(match.group(1)) + int(match.group(2))), code)
    code = re.sub(r'(\d+)\s*\-\s*(\d+)', lambda match: str(int(match.group(1)) - int(match.group(2))), code)

    # --- Flow Control Simplifications ---
    # Simplify while loops with obfuscated conditions
    code = re.sub(r'while\s*\(.*?\)\s*do', 'while true do', code)  # Simplify obfuscated while loop conditions
    
    # --- Generic Patterns ---
    # Add comments for loadstring calls
    code = re.sub(r'loadstring\((.*?)\)', r'-- Decompiled loadstring: \1', code)  # Simulate decompiling loadstring calls
    
    # Remove complex patterns or unnecessary extra characters
    code = re.sub(r'[^\S\n]+$', '', code, flags=re.MULTILINE)  # Clean up trailing spaces on lines
    
    return code

# --- Full Processing Pipeline ---
def process_lua_code(file_path):
    with open(file_path, 'r') as file:
        lua_code = file.read()

    lua_code = decode_strings(lua_code)
    variables, functions = parse_lua_code(lua_code)
    
    # Deobfuscate variables and functions with sequential names
    lua_code = deobfuscate_variables(lua_code, variables)
    lua_code = deobfuscate_functions(lua_code, functions)
    
    # Add newlines after semicolons and ensure new lines
    lua_code = add_newlines_after_semicolons(lua_code)
    
    # Apply makeshift decompiler
    lua_code = makeshift_decompiler(lua_code)
    
    # Beautify the code
    lua_code = beautify_code(lua_code)

    return lua_code

# --- Main Function ---
def main():
    input_file_path = 'C:\\Users\\Administrator\\Documents\\obfuscated.lua'
    processed_code = process_lua_code(input_file_path)

    output_path = 'C:\\Users\\Administrator\\Desktop\\luadeobfuscated.lua'
    with open(output_path, 'w') as output_file:
        output_file.write(processed_code)

    print(f"Processed Lua code has been saved to {output_path}.")
    input("Press Enter to close the script.")

# Execute the main function
if __name__ == "__main__":
    main()
