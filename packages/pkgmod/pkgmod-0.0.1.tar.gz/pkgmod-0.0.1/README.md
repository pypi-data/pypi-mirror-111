# pkgmod
Get module names from installed package names and back.

Example usage:
```python
>>> import pkgmod
>>> pkgmod.get_package_name("impala")
('impyla', False)
```
This returns a tuple with package name and a bool, which tells whether it's
a standard library in Python or not.
For packages this only works if the package is installed.

```python
>>> pkgmod.get_module_names("impyla")
['impala']
>>> pkgmod.get_module_names("Cython")
['Cython', 'cython', 'pyximport']
```
This returns the module names included in a given package (which also needs to
be installed).