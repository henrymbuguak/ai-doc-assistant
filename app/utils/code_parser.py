import ast

def parse_code(code):
    tree = ast.parse(code)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    return {"functions": functions, "classes": classes}

def extract_functions_and_classes(code):
    """
    Extract functions and classes from Python code using AST.
    """
    tree = ast.parse(code)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    return functions, classes

def extract_function_signature(func_node):
    """
    Extract function signature (name, args, returns).
    """
    args = [arg.arg for arg in func_node.args.args]
    returns = ast.unparse(func_node.returns) if func_node.returns else None
    return {
        "name": func_node.name,
        "args": args,
        "returns": returns
    }

def extract_class_metadata(class_node):
    """
    Extract class metadata (name, methods, docstring).
    """
    methods = [node.name for node in ast.walk(class_node) if isinstance(node, ast.FunctionDef)]
    docstring = ast.get_docstring(class_node)
    return {
        "name": class_node.name,
        "methods": methods,
        "docstring": docstring
    }