import io
import random
import re
import types
import zipfile

__all__ = ["import_zip_from_bytes"]


def import_zip_from_bytes(zip_bytes: bytes,
                          module_name: str = None,
                          import_init: bool = False,
                          import_main: bool = False,
                          import_tries: int = None,
                          ignored_files: list = None) -> types.ModuleType:
    if module_name is None:
        module_name = "<Module>"
    zip_handler = zipfile.ZipFile(io.BytesIO(zip_bytes))
    module = types.ModuleType(module_name)
    python_scripts = []
    if ignored_files is None:
        ignored_files = []
    for file in zip_handler.filelist:
        if file.filename in ignored_files:
            continue
        module_tree = tuple(filter(lambda folder: folder, file.filename.replace("\\", "/").split("/")))[1:]
        if file.is_dir():
            if len(module_tree):
                current_module = module
                for part in module_tree:
                    if not hasattr(current_module, part):
                        setattr(current_module, part, types.ModuleType(part))
                    current_module = getattr(current_module, part)
        elif file.filename.endswith(".py"):
            script_name_ = module_tree[-1].split(".")[0]
            if not re.match(re.compile(r"^[a-zA-Z_]+[a-zA-Z0-9_]*$", re.M), script_name_):
                script_name_ = ""  # is not a valid module
            python_scripts.append((file.filename, module_tree[:-1], script_name_, 0, None))
    if import_tries is None:
        import_tries = len(python_scripts) ** 2
    pending_modules = {}
    while python_scripts:
        random.shuffle(python_scripts)
        filename, script_tree, script_name, tries, script_content = python_scripts.pop()
        if tries < import_tries:
            if script_content is None:
                script_content = zip_handler.read(filename)
                expression = re.compile(b"^from\\s+\\.\\w+\\s+import\\s+.*", re.M)
                imports = re.findall(expression, script_content)
                if imports:
                    for import_ in imports:
                        new_import = b""
                        dependency_name = re.search(b"from\\s\\.\\w+", re.sub(b"\\s+", b" ", import_)).group()[6:]
                        expression = re.compile(b"^from\\s+\\..+\\s+import\\s+", re.M)
                        temp = re.sub(expression, b"", import_).replace(b"\n", b"").replace(b"\r", b"")
                        values = re.split(b"\\s*,\\s*", temp)
                        for value in values:
                            new_import += value + b" = " + dependency_name + b"." + value + b"\r\n"
                        script_content = script_content.replace(import_, new_import)
            try:
                current_module = module
                for part in script_tree:
                    current_module = getattr(current_module, part)
                if script_name == "__main__":
                    if import_main:
                        exec(script_content, current_module.__dict__, current_module.__dict__)
                    continue
                elif script_name == "__init__":
                    if import_init:
                        exec(script_content, current_module.__dict__, current_module.__dict__)
                    continue
                if not pending_modules.get(filename):
                    pending_modules[filename] = types.ModuleType(script_name)
                try:
                    exec(script_content, pending_modules[filename].__dict__, pending_modules[filename].__dict__)
                    setattr(current_module, script_name, pending_modules[filename])
                except (NameError, AttributeError):
                    try:
                        pending_modules[filename].__dict__.update(current_module.__dict__)
                        exec(script_content, pending_modules[filename].__dict__, pending_modules[filename].__dict__)
                        setattr(current_module, script_name, pending_modules[filename])
                    except (NameError, AttributeError) as e:
                        raise e
            except (NameError, AttributeError):
                tries += 1
                python_scripts.append((filename, script_tree, script_name, tries, script_content))
    return module
