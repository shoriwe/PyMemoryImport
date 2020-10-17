# PyMemoryImport
 Import python modules (zip archives and scripts) from memory
 
 # Description
 Just a `Python PoC` for importing `"Pure Python"` modules from memory
 
 # Usage
 ## Import script
 You can import a module script by simply doing
 ```python
import types
module = types.ModuleType(module_name)
exec(bytes_of_the_script, module.__dict__, module.__dict__)
# Now you can use "module" as a regular Python module
```
If you only want a method for this you check the `PyMemoryImport/import_script.py` implementation to the just only do
```python
import PyMemoryImport.import_script
module = PyMemoryImport.import_script.import_script_from_bytes(script_content)
# Now you can use "module" as a regular Python module
```
## Import zip
This is a bit more complicated since a python `package` can has sub folders (which are sub-packages) and scripts (which are sub-modules), etc.
A valid zip is just a pure python zipped package
```python
import PyMemoryImport.import_zip
module = PyMemoryImport.import_zip.import_zip_from_bytes(zip_package_bytes)
# Now you can use "module" as a regular Python module
```

 
