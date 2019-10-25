import os.path as osp
import sys
from pathlib import Path


def scan_package(path, base_dir='.'):
    """
    Scan for all the python packages under a certain path. Note that this
    will automatically append the scan path to the PYTHONPATH. You should be
    careful if there is some packages with the same name. In the case of a
    name collision, latter scanned packages will not be imported.

    Args:
        path (str): The path which all the packages under it will be
            imported. You should provide the package path rather than the
            package name.
        base_dir (str, optional): The base directory to be used as a import root.
            Assume the project structure is like:
            .
            ├── package1
            │   └── foo.py
            └── setup.py
            Without setting base_dir, which will automatically take your
            scan root as the import root.
            >>> scan_package('package1')
            Which is equivalent to
            >>> import foo
            If you specify the scan root,
            >>> scan_package('package1', 'package1')
            this function will use the given root:
            >>> import package1.foo

            However, you should never let a scan root to be empty if the package
            to be scanned is a regular package (with __init__.py inside).
            .
            ├── package2
            │   ├── __init__.py
            │   └── foo.py
            └── setup.py
            This will raise a ValueError:
            >>> scan_package('package2', 'package2')
            Which is equivalent to
            >>> import .

    Raise:
        ValueError:
            - path does not exist
            - base_dir does not exist
            - base_dir is not valid for importing
    """
    abs_path = osp.abspath(path)
    if not osp.exists(abs_path):
        raise ValueError('Parameter `path`: {} not exist'.format(abs_path))
    if not osp.exists(base_dir):
        raise ValueError('Parameter `base_dir`: {} does not exist'.format(base_dir))

    base_dir = osp.abspath(base_dir)
    if not abs_path.startswith(base_dir):
        raise ValueError('`path`: {} is not a subdirectory of `base_dir`: {}'
                         .format(abs_path, base_dir))

    # mark the base directory as source root
    sys.path.insert(0, base_dir)

    # scan for all **/*.py file under certain dir
    modules = [f for f in Path(abs_path).rglob('*.py') if f.is_file()]
    # set **/__init__.py to the package name
    modules = [f.parent if f.name == '__init__.py' else f for f in modules]

    # import all modules
    for module in modules:
        module_rel_path = module.relative_to(base_dir)
        # check for invalid regular package import
        if str(module_rel_path) == '.':
            raise ValueError('You may want to import package {} with the scan root as the package, '
                             ', which will cause a importing error. Please try some scan roots outside'
                             'the package')
        else:
            module_name = '.'.join(module_rel_path.with_suffix('').parts)
        # check if the package has been imported
        if module_name not in sys.modules.keys():
            __import__(module_name)
