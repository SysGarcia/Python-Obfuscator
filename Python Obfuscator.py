import ast
import itertools
import random
import re

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

def get_funny_strings(level_of_obfuscation: int) -> list:
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
    for x in length_strings('0O'):
        all_possible_combinations.append("I"+''.join(x))
    return all_possible_combinations

code = """
a = "#Zxc"
print(a) #zxcased

"""
found_items = analyze_code(code)

def replacements(found_items: dict) -> dict:
    global funny_strings
    """
    Generates a dictionary mapping original names to obfuscated names.

    Parameters:
    found_items (dict): A dictionary containing sets of elements to obfuscate.

    Returns:º
    dict: A dictionary mapping original names to obfuscated names.
    """
    funny_strings = get_funny_strings(18)
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

def generate_random_comment():
    comments = [
        "# Interesting approach, line 16",
        "# Optimizing performance  line 96",
        "# This part is crucial  line 32",
        "# Generated comment  line 125",
        "# Placeholder comment  line 112",
        "# TODO: Review this later  line 178",
        "# This might need refactoring  line 224",
        "# Why was this done this way?  line 122",
        "# Magic happens here  line 4",
        "# Be careful with this part  line 1"
    ]
    return random.choice(comments)

code.replace("\n","\\n")
code=ast.unparse(ast.parse(code))

def rename_elements(code, replacements):
    pattern = r'\b(' + '|'.join(re.escape(key) for key in replacements.keys()) + r')\b'
    
    lines_of_code = code.split('\n')
    new_lines = []

    for line in lines_of_code:
        # Randomly decide whether to insert a comment on this line
        if random.random() < 0.3:  # Adjust the probability as needed
            # Insert a comment before the line
            new_lines.append(generate_random_comment())
        new_lines.append(line)
    
    code_with_comments = '\n'.join(new_lines)
    
    # Replace all occurrences of names in the code based on the replacements dictionary
    return re.sub(pattern, lambda m: replacements.get(m.group(0), m.group(0)), code_with_comments)

replacements_dict = replacements(found_items)
new_code = rename_elements(code, replacements_dict)

print(new_code)
