import re

# --- Load Lua Code ---
def load_lua_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# --- Save Updated Lua Code ---
def save_lua_code(file_path, code):
    with open(file_path, 'w') as file:
        file.write(code)

# --- Find Variables and Functions ---
def find_identifiers(code):
    # Use regex to find local variables and function names
    variables = re.findall(r'local\s+([\w_]+)\s*=', code)
    functions = re.findall(r'function\s+([\w_]+)\s*\(', code)
    return variables, functions

# --- Rename Variables ---
def rename_variables(code, variables):
    new_names = {}
    print("Manual Variable Renaming:")
    
    for var in variables:
        # Suggest a new variable name based on user input
        new_name = input(f"Enter a new name for variable '{var}' (or press Enter to skip): ").strip()
        if new_name:
            new_names[var] = new_name

    # Replace variable names in the code
    for old_name, new_name in new_names.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)

    return code, new_names

# --- Rename Functions ---
def rename_functions(code, functions):
    new_names = {}
    print("Manual Function Renaming:")
    
    for func in functions:
        # Suggest a new function name based on user input
        new_name = input(f"Enter a new name for function '{func}' (or press Enter to skip): ").strip()
        if new_name:
            new_names[func] = new_name

    # Replace function names in the code
    for old_name, new_name in new_names.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)

    return code, new_names

# --- Main Manual Renaming Function ---
def manual_renamer(lua_code_path):
    lua_code = load_lua_code(lua_code_path)

    # Step 1: Find all local variables and functions
    variables, functions = find_identifiers(lua_code)

    # Step 2: Rename variables manually
    lua_code, renamed_vars = rename_variables(lua_code, variables)

    # Step 3: Rename functions manually
    lua_code, renamed_funcs = rename_functions(lua_code, functions)

    # Step 4: Save the updated Lua code
    output_path = lua_code_path.replace('.lua', '_renamed.lua')
    save_lua_code(output_path, lua_code)

    print(f"\nRenaming completed! Updated Lua code has been saved to {output_path}.")

# --- Entry Point ---
if __name__ == "__main__":
    lua_code_path = input("Enter the path to the Lua file to rename: ").strip()
    manual_renamer(lua_code_path)
