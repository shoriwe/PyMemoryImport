import types

__all__ = ["import_script_from_bytes"]


def import_script_from_bytes(module_name: str, script_bytes: bytes) -> types.ModuleType:
    script_module = types.ModuleType(module_name)
    exec(script_bytes, script_module.__dict__, script_module.__dict__)
    return script_module
