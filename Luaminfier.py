import re
import os
import base64

# IF YOUR MINIFIER CLOSES ON ITSELF, YOU HAVE DONE SOMETHING WRONG CONTACT ME ON MY GMAIL
# MAKE SURE TO ENTER THE FILE YOU WANT TO DEOBFUSCATE OR MINIMIZE TO YOUR ADMINISTRATOR ACCOUNT
# UNDER THE DOCUMENTS FOLDER AND MAKE SURE THE FILE IS NAMED obfuscated.lua !!!
# ALSO IM UNDER THE C:\ DRIVE CHANGE TO YOUR WILL UNDER LINE 69 AND 72


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

# --- Lua Parsing Functions ---
def parse_lua_code(code):
    variables = re.findall(r'local\s+([\w_]+)\s*=', code)
    functions = re.findall(r'function\s+([\w_]+)\s*\(', code)
    return variables, functions

def deobfuscate_variables(code, variables):
    for var in variables:
        code = re.sub(r'\b' + re.escape(var) + r'\b', 'deobf_' + var, code)
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

# --- Full Processing Pipeline ---
def process_lua_code(file_path):
    with open(file_path, 'r') as file:
        lua_code = file.read()

    lua_code = decode_strings(lua_code)
    variables, _ = parse_lua_code(lua_code)
    lua_code = deobfuscate_variables(lua_code, variables)
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
