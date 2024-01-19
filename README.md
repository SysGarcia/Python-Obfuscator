# Python Code Obfuscator

## Description
This Python Code Obfuscator is a tool designed to modify Python source code by renaming various elements such as variables, functions, classes, and parameters. The tool aims to make the source code harder to read and understand, thus providing a layer of obfuscation.

## Features
- **AST-Based Analysis**: Uses the Abstract Syntax Tree (AST) for analyzing the Python code, ensuring accurate identification of elements to be renamed.
- **Customizable Obfuscation**: Generates a set of 'funny' strings used for renaming, with adjustable complexity and length.
- **Exclusion of Magic Methods**: Ignores special Python methods (`__init__`, `__str__`, etc.) to preserve functionality.
- **Global Replacement**: Renames elements throughout the code, including within string literals.

## Usage
1. **Analyzing the Code**: The tool first analyzes the given Python code to find all the variables, functions, classes, and parameters using the `CodeAnalyzer` class.
2. **Generating Replacements**: It then generates a mapping of original names to obfuscated names using the `replacements` function.
3. **Renaming Elements**: Finally, the `rename_elements` function applies these replacements to the entire code, including string literals.

### Example
```python
code = "<Your Python Code Here>"
found_items = analyze_code(code)
replacements_dict = replacements(found_items)
obfuscated_code = rename_elements(code, replacements_dict)
print(obfuscated_code)
```
## Important Notes
- The obfuscator currently does not differentiate between string literals and other code. This means that strings containing names that match variables, functions, or classes will also be renamed.
- The obfuscator might affect the functionality of the code if it relies on specific names (e.g., dynamic attribute access, metaprogramming).
