import PyMemoryImport.import_script
import PyMemoryImport.import_zip


def test_script_module_import():
    script_module_bytes = open("Modules/script_module.py", "rb").read()
    script_module = PyMemoryImport.import_script.import_script_from_bytes("a_module", script_module_bytes)
    script_module.hello_script()


def test_directory_module_import():
    zip_module_bytes = open("Modules/dir_module.zip", "rb").read()
    zip_module = PyMemoryImport.import_zip.import_zip_from_bytes("zip_module", zip_module_bytes)
    zip_module.hello_init()
    zip_module.hello_from_sub_module_functions()
    zip_module.sub_module.sub_module_functions.hello_from_sub_module_functions()


def main():
    print("testing the import from a script's bytes...")
    test_script_module_import()
    print("\ntesting the import from a zip archived module directory")
    test_directory_module_import()


if __name__ == '__main__':
    main()