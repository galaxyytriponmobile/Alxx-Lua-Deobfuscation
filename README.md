# 🐍 Python to Lua Converter

**Luaminifier.py** and **Luaminf.manual.py**: Utilities to make your Lua scripts more readable and manageable. ✔️

---

## ⚠️ IMPORTANT NOTICE: READ BEFORE STARTING THE SCRIPT! ⚠️
------------------------------------------------------------
🚨 **DO NOT EXECUTE THE CODE WITHOUT FOLLOWING THESE INSTRUCTIONS!** 🚨  
Make sure to **TWEAK THE CODE** at **Line 173** and **Line 176** in `luaminifier.py` before running the script.  
------------------------------------------------------------  

**Potential Issues**  
If the script **closes unexpectedly**, you may have misconfigured it during the tweaks.  
Please **double-check** your adjustments before trying again.

---

## 🛠️ **Scripts Overview**

### 1. **Luaminifier.py**
A Python-based tool designed to enhance the readability of obfuscated Lua scripts. It performs deobfuscation by renaming variables and functions, improving the formatting by adjusting indentation and semicolons, and adding several additional Lua code optimizations such as:

- **Variable & Function Deobfuscation**: Automatically renames variables and functions to improve readability.
- **Beautification**: Adjusts indentation and formats code for cleaner presentation.
- **Makeshift Decompiler**: Attempts to reverse certain types of Lua obfuscation patterns, simplifying the code further.
- **Handling Encoded Strings**: Decodes base64-encoded and hex-encoded strings in the Lua code.
- **Optimized for Performance**: Regex optimizations and error handling for better script performance.

### 2. **Luaminf.manual.py**
A complementary script to **Luaminifier.py**. This tool offers **manual renaming** of variables and functions after the initial deobfuscation process, giving users full control over making Lua scripts readable and maintainable.

#### Features:
- **Interactive Renaming**: Detects all variables and functions in the deobfuscated Lua script and prompts the user for more meaningful names.
- **File Handling**: Automatically saves the updated Lua script to a new file with all manual renaming applied.
- **Improved Script Management**: Allows you to clean up poorly named variables and functions in a Lua script, making it human-readable and easier to maintain.

---

## 📋 **Changelog**:

### **UPDATE 1**:  
- Improved the code by renaming functions, variables, etc., to numbers, increasing readability.  
- Started removing semicolons for better formatting.  

### **UPDATE 2**:  
- Semicolon removal **completed**.  

### **UPDATE 3**:  
- Now adds a **new line** after encountering closing characters `)`, `}`, `]`.

### **UPDATE 4**:  
- **Re-added semicolons** to improve readability.

### 🔥 **UPDATE 5: DECOMPILER FEATURE ADDED!** 🔥  
- A makeshift decompiler has been implemented—check it out!

### **UPDATE 6**:  
- Inserted a space before the keyword `"local"` for better formatting.

### **UPDATE 7**:  
- Additional features added to the makeshift decompiler.

---

### 🔥 **UPDATE 8 (LATEST)** 🔥  
- **Enhanced Error Handling**: Added try-except blocks to manage file operations and decoding errors.  
- **Refactoring**: Merged `deobfuscate_variables` and `deobfuscate_functions` into a reusable `deobfuscate_names` function for more maintainable code.  
- **Regex Optimization**: Simplified regular expressions for better performance.  
- **Edge Case Handling**: Improved handling of missing or malformed Lua code files.  
- **Logging & Error Feedback**: Replaced prints with meaningful error feedback for better issue tracing.

---

## 🚀 **How to Use**:

### Step 1: Run **Luaminifier.py** to Deobfuscate Lua Code
1. Open a terminal or command line in the directory containing the `luaminifier.py` script.
2. Ensure you've updated **Line 173** and **Line 176** with your file paths.
3. Run the script to deobfuscate your Lua code:
    ```bash
    python luaminifier.py
    ```

### Step 2: Run **Luaminf.manual.py** for Manual Renaming
1. Once your Lua code is deobfuscated, run `luaminf.manual.py` to manually rename variables and functions for better readability.
2. This will prompt you to input new names for each detected variable and function:
    ```bash
    python luaminf.manual.py
    ```
3. The manually renamed Lua script will be saved as a new file (e.g., `my_lua_script_renamed.lua`).

---

## 🛠️ **Planned Features**:
- Integration of more advanced decompilation techniques.
- Automating the manual renaming process based on predefined patterns.
- Improving edge case handling for more complex obfuscated scripts.
