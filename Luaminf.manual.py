import re

# --- Load Lua Code ---
def load_lua_code(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# --- Save Updated Lua Code ---
def save_lua_code(file_path, code):
    with open(file_path, 'w') as file:
        file.write(code)

# --- Find Variables and Functions ---
def find_identifiers(code):
    variables = re.findall(r'local\s+([\w_]+)\s*=', code)
    functions = re.findall(r'function\s+([\w_]+)\s*\(', code)
    return variables, functions

# --- Predefined Renaming Patterns (Automating Manual Renaming) ---
def predefined_renaming(identifiers, prefix):
    new_names = {}
    for idx, name in enumerate(identifiers, start=1):
        new_name = f"{prefix}_{idx}"
        new_names[name] = new_name
    return new_names

# --- Rename Variables ---
def rename_variables(code, variables):
    print("Manual or Automated Variable Renaming:")
    use_auto = input("Do you want to use automated renaming for variables? (y/n): ").strip().lower()

    if use_auto == 'y':
        prefix = input("Enter prefix for variable renaming (e.g., 'var'): ").strip()
        new_names = predefined_renaming(variables, prefix)
    else:
        new_names = {}
        for var in variables:
            new_name = input(f"Enter a new name for variable '{var}' (or press Enter to skip): ").strip()
            if new_name:
                new_names[var] = new_name

    # Replace variable names in the code
    for old_name, new_name in new_names.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)

    return code, new_names

# --- Rename Functions ---
def rename_functions(code, functions):
    print("Manual or Automated Function Renaming:")
    use_auto = input("Do you want to use automated renaming for functions? (y/n): ").strip().lower()

    if use_auto == 'y':
        prefix = input("Enter prefix for function renaming (e.g., 'func'): ").strip()
        new_names = predefined_renaming(functions, prefix)
    else:
        new_names = {}
        for func in functions:
            new_name = input(f"Enter a new name for function '{func}' (or press Enter to skip): ").strip()
            if new_name:
                new_names[func] = new_name

    # Replace function names in the code
    for old_name, new_name in new_names.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)

    return code, new_names

# --- Advanced Decompilation Techniques ---
def advanced_decompiler(code):
    # Simplifying more complex patterns such as obfuscated table indexing
    code = re.sub(r'\[\"(.+?)\"\]', r'.\1', code)  # Simplifies table indexing
    code = re.sub(r'function\s*\(.*?\)', 'function(...)', code)  # Simplifies function signatures
    code = re.sub(r'loadstring\((.*?)\)', r'-- Decompiled loadstring: \1', code)  # Handles loadstring patterns
    return code

# --- Main Manual Renaming Function ---
def manual_renamer(lua_code_path):
    lua_code = load_lua_code(lua_code_path)
    if lua_code is None:
        return

    # Step 1: Find all local variables and functions
    variables, functions = find_identifiers(lua_code)

    # Step 2: Advanced decompilation techniques
    lua_code = advanced_decompiler(lua_code)

    # Step 3: Rename variables manually or automatically
    lua_code, renamed_vars = rename_variables(lua_code, variables)

    # Step 4: Rename functions manually or automatically
    lua_code, renamed_funcs = rename_functions(lua_code, functions)

    # Step 5: Save the updated Lua code
    output_path = lua_code_path.replace('.lua', '_renamed.lua')
    save_lua_code(output_path, lua_code)

    print(f"\nRenaming completed! Updated Lua code has been saved to {output_path}.")

# --- Entry Point ---
if __name__ == "__main__":
    lua_code_path = input("Enter the path to the Lua file to rename: ").strip()
    manual_renamer(lua_code_path)
