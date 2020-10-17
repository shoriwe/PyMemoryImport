import types

__all__ = ["import_script_from_bytes"]


def import_script_from_bytes(script_bytes: bytes, module_name: str = None) -> types.ModuleType:
    if module_name is None:
        module_name = "<Module>"
    script_module = types.ModuleType(module_name)
    exec(script_bytes, script_module.__dict__, script_module.__dict__)
    return script_module
