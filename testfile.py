import sys
import subprocess
import re
import os
import base64
import openai

# --- Install OpenAI if not installed ---
def install_openai():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    except subprocess.CalledProcessError:
        print("Failed to install openai. Exiting...")
        sys.exit(1)
        
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
    code = re.sub(r'\bif\s+true\s+then\b', 'if true then', code)
    code = re.sub(r'\bif\s+false\s+then\b', 'if false then', code)
    return code

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
    code = re.sub(r'(\d+)\s*\-\s*(\d+)', lambda m: str(int(m.group(1)) - int(m.group(2))), code)
    code = re.sub(r'while\s*\(.*?\)\s*do', 'while true do', code)
    code = re.sub(r'loadstring\((.*?)\)', r'-- Decompiled loadstring: \1', code)
    code = re.sub(r'[^\S\n]+$', '', code, flags=re.MULTILINE)
    code = re.sub(r'\blocal\b', ' local', code)
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

# --- ChatGPT Query ---
def query_chatgpt(prompt, api_key):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or use gpt-3.5-turbo if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error querying ChatGPT: {e}")
        return None

def main():
    # Step 1: Ask the user to press Enter to proceed
    input("Press Enter to begin the Lua de-obfuscation process...")

    # Ask the user for the OpenAI API key
    api_key = input("Enter your OpenAI API key: ")

    # Ask the user for the Lua script file path
    input_file_path = input("Enter the path to your Lua script file: ")

    # Step 2: Process the Lua script
    processed_code = process_lua_code(input_file_path)

    # Step 3: Send the processed code to ChatGPT for final formatting
    prompt = f"i ran my obfuscated script through alxx-lua-de-obfuscator and i got this. Please change all of the variables and functions, and spacing correctly. Please only give me the output code, changed, no other words. AGAIN, NO OTHER WORDS.\n\n{processed_code}"
    updated_script = query_chatgpt(prompt, api_key)
    
    if updated_script:
        # Step 4: Ask where to save the updated script
        output_path = input("Enter the path where you want to save the deobfuscated Lua script: ")

        # Save the processed and updated Lua script
        with open(output_path, 'w') as output_file:
            output_file.write(updated_script)

        print(f"Processed Lua code has been saved to {output_path}.")
    else:
        print("Failed to get a response from ChatGPT.")
    
    # Step 5: Ask the user to press Enter to close the script
    input("Press Enter to close the script.")

if __name__ == "__main__":
    main()
