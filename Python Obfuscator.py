import ast
import itertools
import random
import re
import string

class CodeAnalyzer(ast.NodeVisitor):
    """
    AST Node Visitor that analyzes Python source code to extract various elements
    like variables, functions, classes, and parameters.
    """
    def __init__(self):
        self.found = {
            "variables": set(),
            "functions": set(),
            "classes": set(),
            "parameters": set()
        }

    def visit_FunctionDef(self, node):
        # Add function names to the found set
        self.found["functions"].add(node.name)
        # Add function parameters to the found set
        for arg in node.args.args:
            self.found["parameters"].add(arg.arg)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Add class names to the found set
        self.found["classes"].add(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Add variable names to the found set
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.found["variables"].add(target.id)
        self.generic_visit(node)

    def report(self):
        """
        Reports the elements found in the source code.

        Returns:
        dict: A dictionary containing sets of found elements.
        """
        return self.found

def analyze_code(code: str) -> dict:
    """
    Analyzes Python source code to find variables, functions, classes, and parameters.

    Parameters:
    code (str): A string containing Python source code.

    Returns:
    dict: A dictionary containing sets of found elements.
    """
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.report()

# Example usage
code = """
Here goes your code #
"""
code.replace("\n","\\n")

def get_funny_strings(VarAprox:int ,level_of_obfuscation: int) -> list:
    """
    Generates a list of obfuscated strings.

    Parameters:
    level_of_obfuscation (int): The length of each obfuscated string.

    Returns:
    list: A list of obfuscated strings.
    """
    def length_strings(obfus_chars):
        yield from itertools.product(*([obfus_chars] * level_of_obfuscation)) 

    all_possible_combinations = []
    letter_choices=["I","R","G","B","M","A"]
    for x in length_strings('0O'):
        all_possible_combinations.append(random.choice(letter_choices)+''.join(x))
        if len(all_possible_combinations) == VarAprox:
            break
    return all_possible_combinations

found_items = analyze_code(code)

def replacements(found_items: dict) -> dict:
    global funny_strings
    """
    Generates a dictionary mapping original names to obfuscated names.

    Parameters:
    found_items (dict): A dictionary containing sets of elements to obfuscate.

    Returns:
    dict: A dictionary mapping original names to obfuscated names.
    """
    funny_strings = get_funny_strings(200,100)
    dict_with_replacements = {}
    
    # Exclude magic methods (like __init__, __str__, etc.)
    magic_methods = {name for name in found_items["functions"] if name.startswith('__') and name.endswith('__')}

    # Iterate over each key in the found_items dictionary
    for key in found_items:
        for item in found_items[key]:
            if item in magic_methods:
                continue
            
            random_index = random.randrange(len(funny_strings))
            funny_string_value = funny_strings[random_index]
            dict_with_replacements.update({item: funny_string_value})
            funny_strings.pop(random_index)
    
    return dict_with_replacements

def rename_elements(code, replacements):
    """
    This function renames elements in the provided Python code. It ensures that
    only specific elements (like variable names, function names, etc.) are renamed,
    while string literals remain unchanged.

    Parameters:
    - code (str): The Python source code as a string.
    - replacements (dict): A dictionary where each key is an original name in the code
      that needs to be replaced, and its value is the new name for that element.

    Returns:
    - str: The modified Python source code with elements renamed as specified
      in the replacements dictionary.
    """
    pattern = r'\b(' + '|'.join(re.escape(key) for key in replacements.keys()) + r')\b'

    # Replace all occurrences of names in the code based on the replacements dictionary
    return re.sub(pattern, lambda m: replacements.get(m.group(0), m.group(0)), code)

replacements_dict = replacements(found_items)
new_code = rename_elements(code, replacements_dict)

print(new_code)
