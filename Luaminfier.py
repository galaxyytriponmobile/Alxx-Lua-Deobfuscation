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
    code = re.sub(r';', ';\n', code)
    code = re.sub(r'(\)|\}|\])', r'\1\n', code)
    lines = code.splitlines()
    formatted_code = '\n'.join(line.strip() for line in lines if line.strip())
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
        deobf_var = f'deobf_var_{counter}'
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

# --- New Deobfuscation Features ---
def simplify_boolean_expressions(code):
    # Simplify boolean expressions like "if true then" to "if true then"
    code = re.sub(r'\bif\s+true\s+then\b', 'if true then', code)
    code = re.sub(r'\bif\s+false\s+then\b', 'if false then', code)
    return code

def simplify_string_concatenation(code):
    # Simplify concatenation of string literals, e.g., "hello" .. "world" -> "helloworld"
    return re.sub(r'"([^"]+)"\s*\.\.\s*"([^"]+)"', lambda m: f'"{m.group(1)}{m.group(2)}"', code)

def decode_hex_strings(code):
    # Convert hexadecimal strings to plain text if detected
    return re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), code)

def unroll_loops(code):
    # Unroll basic loops for constant ranges
    def loop_unroll(match):
        var, start, end = match.groups()
        return '\n'.join([f'{var} = {i}' for i in range(int(start), int(end) + 1)])

    return re.sub(r'for\s+(\w+)\s*=\s*(\d+),\s*(\d+)\s*do', loop_unroll, code)

def preserve_comments(code):
    # Capture and preserve comments in obfuscated code
    return re.sub(r'--.*', lambda m: f'{m.group(0)}', code)

# --- Makeshift Decompiler with Enhanced Features ---
def makeshift_decompiler(code):
    # Simplify function definitions
    code = re.sub(r'function\s*\(.*?\)', 'function(...)', code)
    
    # Simplify obfuscated loops
    code = re.sub(r'for\s*([\w_]+)\s*=.*?do', r'for \1 = ... do', code)
    
    # Simplify complex conditions
    code = re.sub(r'if\s*\(.*?\)\sthen', 'if condition then', code)
    
    # Reverse string obfuscation patterns
    code = re.sub(r'string\.char\(([\d, ]+)\)', lambda m: ''.join(chr(int(x)) for x in m.group(1).split(',')), code)
    
    # Simplify tables with numbered keys
    code = re.sub(r'\[(\d+)\]\s*=\s*', '', code)
    
    # Handle inline function patterns
    code = re.sub(r'\w+\(\s*function\s*\(.*?\)\s*', 'function(...) ', code)
    
    # Simplify math expressions
    code = re.sub(r'(\d+)\s*\+\s*(\d+)', lambda m: str(int(m.group(1)) + int(m.group(2))), code)
    code = re.sub(r'(\d+)\s*\-\s*(\d+)', lambda m: str(int(m.group(1)) - int(m.group(2))), code)
    
    # Simplify while loops
    code = re.sub(r'while\s*\(.*?\)\s*do', 'while true do', code)
    
    # Add comments for loadstring
    code = re.sub(r'loadstring\((.*?)\)', r'-- Decompiled loadstring: \1', code)
    
    # Clean up trailing spaces
    code = re.sub(r'[^\S\n]+$', '', code, flags=re.MULTILINE)
    
    # Add space around "local"
    code = re.sub(r'\blocal\b', ' local ', code)
    
    # Apply new features
    code = simplify_boolean_expressions(code)
    code = simplify_string_concatenation(code)
    code = decode_hex_strings(code)
    code = unroll_loops(code)
    code = preserve_comments(code)

    return code

# --- Full Processing Pipeline ---
def process_lua_code(file_path):
    with open(file_path, 'r') as file:
        lua_code = file.read()

    lua_code = decode_strings(lua_code)
    variables, functions = parse_lua_code(lua_code)
    
    lua_code = deobfuscate_variables(lua_code, variables)
    lua_code = deobfuscate_functions(lua_code, functions)
    
    lua_code = add_newlines_after_semicolons(lua_code)
    
    lua_code = makeshift_decompiler(lua_code)
    
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
