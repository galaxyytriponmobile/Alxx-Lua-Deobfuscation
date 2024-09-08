import re
import os
import base64

# --- Beautifier Function ---
def beautify_code(code):
    indent_level = 0
    beautified_code = []
    indent_keywords = {'function', 'if', 'else', 'elseif', 'for', 'while', 'do'}
    unindent_keywords = {'end', 'else', 'elseif'}
    lines = re.split(r'(\b(?:function|if|else|elseif|for|while|do|end)\b|\n|;)', code)

    for line in lines:
        stripped_line = line.strip()

        if stripped_line in unindent_keywords:
            indent_level = max(indent_level - 1, 0)

        if stripped_line:
            beautified_code.append('    ' * indent_level + stripped_line)

        if stripped_line in indent_keywords:
            indent_level += 1

    return '\n'.join(beautified_code).strip()

# --- Add New Line After Semicolons and Ensure New Lines ---
def add_newlines_after_semicolons(code):
    code = re.sub(r';', ';\n', code)
    code = re.sub(r'(\)|\}|\])', r'\1\n', code)
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    return '\n'.join(lines)

# --- Lua Parsing Functions ---
def parse_lua_code(code):
    variables = re.findall(r'local\s+([\w_]+)\s*=', code)
    functions = re.findall(r'function\s+([\w_]+)\s*\(', code)
    return variables, functions

def deobfuscate_names(code, names, prefix):
    deobf_map = {name: f'{prefix}_{i + 1}' for i, name in enumerate(names)}
    for old_name, new_name in deobf_map.items():
        code = re.sub(rf'\b{re.escape(old_name)}\b', new_name, code)
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
    return re.sub(r'\bif\s+(true|false)\s+then\b', r'if \1 then', code)

def simplify_string_concatenation(code):
    return re.sub(r'"([^"]+)"\s*\.\.\s*"([^"]+)"', lambda m: f'"{m.group(1)}{m.group(2)}"', code)

def decode_hex_strings(code):
    return re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), code)

def unroll_loops(code):
    def loop_unroll(match):
        var, start, end = match.groups()
        return '\n'.join([f'{var} = {i}' for i in range(int(start), int(end) + 1)])
    return re.sub(r'for\s+(\w+)\s*=\s*(\d+),\s*(\d+)\s*do', loop_unroll, code)

def preserve_comments(code):
    return re.sub(r'--.*', lambda m: f'{m.group(0)}', code)

# --- Makeshift Decompiler with Enhanced Features ---
def makeshift_decompiler(code):
    code = re.sub(r'function\s*\(.*?\)', 'function(...)', code)
    code = re.sub(r'for\s*([\w_]+)\s*=.*?do', r'for \1 = ... do', code)
    code = re.sub(r'if\s*\(.*?\)\sthen', 'if condition then', code)
    code = re.sub(r'string\.char\(([\d, ]+)\)', lambda m: ''.join(chr(int(x)) for x in m.group(1).split(',')), code)
    code = re.sub(r'\[(\d+)\]\s*=\s*', '', code)
    code = re.sub(r'\w+\(\s*function\s*\(.*?\)\s*', 'function(...) ', code)
    code = re.sub(r'(\d+)\s*\+\s*(\d+)', lambda m: str(int(m.group(1)) + int(m.group(2))), code)
    code = re.sub(r'while\s*\(.*?\)\s*do', 'while true do', code)
    code = re.sub(r'loadstring\((.*?)\)', r'-- Decompiled loadstring: \1', code)
    code = re.sub(r'[^\S\n]+$', '', code, flags=re.MULTILINE)
    code = re.sub(r'\blocal\b', ' local', code)

    # Apply new features
    code = simplify_boolean_expressions(code)
    code = simplify_string_concatenation(code)
    code = decode_hex_strings(code)
    code = unroll_loops(code)
    code = preserve_comments(code)

    return code

# --- Full Processing Pipeline ---
def process_lua_code(file_path):
    try:
        with open(file_path, 'r') as file:
            lua_code = file.read()

        lua_code = decode_strings(lua_code)
        variables, functions = parse_lua_code(lua_code)
        
        lua_code = deobfuscate_names(lua_code, variables, 'deobf_var')
        lua_code = deobfuscate_names(lua_code, functions, 'deobf_func')
        
        lua_code = add_newlines_after_semicolons(lua_code)
        lua_code = makeshift_decompiler(lua_code)
        lua_code = beautify_code(lua_code)

        return lua_code
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# --- Main Function ---
def main():
    input_file_path = 'C:\\Users\\Administrator\\Documents\\obfuscated.lua'
    output_file_path = 'C:\\Users\\Administrator\\Desktop\\luadeobfuscated.lua'

    processed_code = process_lua_code(input_file_path)

    if processed_code:
        try:
            with open(output_file_path, 'w') as output_file:
                output_file.write(processed_code)
            print(f"Processed Lua code has been saved to {output_file_path}.")
        except Exception as e:
            print(f"Failed to save file: {e}")
    else:
        print("No code processed. Exiting.")

if __name__ == "__main__":
    main()
