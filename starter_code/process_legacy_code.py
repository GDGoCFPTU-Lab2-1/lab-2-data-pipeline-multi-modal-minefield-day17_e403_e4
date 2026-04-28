import ast
from datetime import datetime
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # Use the 'ast' module to find docstrings for functions
    parsed = ast.parse(source_code)
    docstrings = []
    for node in ast.walk(parsed):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings.append(f"Function {node.name}:\n{docstring}")
    
    # Use regex to find business rules in comments like "# Business Logic Rule 001"
    rules = re.findall(r'#\s*Business Logic Rule\s*\d+:.*', source_code, re.IGNORECASE)
    
    # Also find any tax calculation comments to trigger quality gate test later
    tax_comments = re.findall(r'#.*tax.*', source_code, re.IGNORECASE)
    
    content = "Docstrings:\n" + "\n".join(docstrings) + "\n\nComments:\n" + "\n".join(rules) + "\n" + "\n".join(tax_comments)
    
    # Return a dictionary for the UnifiedDocument schema.
    return {
        "document_id": "code-legacy-1",
        "content": content,
        "source_type": "Code",
        "author": "Legacy Developer",
        "timestamp": datetime.now().isoformat(),
        "source_metadata": {}
    }
