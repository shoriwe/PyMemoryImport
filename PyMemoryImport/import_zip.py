import io
import random
import re
import types
import zipfile


__all__ = ["import_zip_from_bytes"]


def _get_module_path(file_path: str) -> tuple:
    return tuple(filter(lambda folder: folder, file_path.replace("\\", "/").split("/")))[1:]


def _calculate_deep(file_path: str) -> int:
    return file_path.replace("\\", "/").count("/")


def import_zip_from_bytes(module_name: str, zip_bytes: bytes) -> types.ModuleType:
    zip_file_handler = zipfile.ZipFile(io.BytesIO(zip_bytes))
    zip_module = types.ModuleType(module_name)
    files = []
    file: zipfile.ZipInfo
    for file in zip_file_handler.filelist:
        module_path = _get_module_path(file.filename)
        if file.is_dir():
            if _calculate_deep(file.filename) > 1:
                current_module = zip_module
                for part in module_path:
                    if not hasattr(current_module, part):
                        setattr(current_module, part, types.ModuleType(part))
                    current_module = getattr(current_module, part)
        elif any(file.filename.endswith(extension) for extension in (".py",)):
            script_as_module: str
            script_as_module = module_path[-1].split(".")[0]
            if "." in script_as_module:
                script_as_module = ""
            files.append((file.filename, module_path[:-1], script_as_module, 0, None))
    while files:
        random.shuffle(files)
        filename, module_path, script_as_module, tries, script_content = files.pop()
        if tries < 100:
            if script_content is None:
                script_content = zip_file_handler.read(filename)
                expression = re.compile(b"^from\s+\.\w+\s+import\s+.*", re.M)
                imports = re.findall(expression, script_content)
                if imports:
                    for import_ in imports:
                        new_import = b""
                        dependency_name = re.search(b"from\s\.\w+", re.sub(b"\s+", b" ", import_)).group()[6:]
                        expression = re.compile(b"^from\s+\..+\s+import\s+", re.M)
                        temp = re.sub(expression, b"", import_).replace(b"\n", b"").replace(b"\r", b"")
                        values = re.split(b"\s*,\s*", temp)
                        for value in values:
                            new_import += value + b" = " + dependency_name + b"." + value + b"\r\n"
                        script_content = script_content.replace(import_, new_import)
                        # print(script_content.decode())
            try:
                current_module = zip_module
                for part in module_path:
                    current_module = getattr(current_module, part)
                script_module = types.ModuleType(script_as_module)
                try:
                    exec(script_content, script_module.__dict__, script_module.__dict__)
                    setattr(current_module, script_as_module, script_module)
                except Exception as e:
                    try:
                        script_module.__dict__.update(current_module.__dict__)
                        exec(script_content, script_module.__dict__, script_module.__dict__)
                        setattr(current_module, script_as_module, script_module)
                    except Exception as e:
                        raise e
            except Exception as e:
                tries += 1
                files.append((filename, module_path, script_as_module, tries, script_content))
    return zip_module
