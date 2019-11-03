import re
from abc import ABC
from typing import TypeVar, List

import pinject
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .controller import Controller
from .package_scanner import scan_package

T = TypeVar('T')

"""Context for holding object graph"""
__context__: pinject.object_graph.ObjectGraph


def get_arg_names_from_class_name(class_name: str):
    """Converts normal class names into normal arg names.

    Normal class names are assumed to be CamelCase with an optional leading
    underscore.  Normal arg names are assumed to be lower_with_underscores.

    Args:
      class_name: a class name, e.g., "FooBar" or "_FooBar"
    Returns:
      all likely corresponding arg names, e.g., ["foo_bar"]
    """
    parts = []
    # preprocess format like 'Foo_bar', '_FooBar' and 'foo_bar' to CamelCase
    rest = ''.join(map(lambda x: x[0:1].upper() + x[1:], class_name.split('_')))
    # slice by the Camel pattern
    while True:
        m = re.match(r'([A-Z]+?[a-z]*)(.*)', rest)
        if m is None:
            break
        parts.append(m.group(1))
        rest = m.group(2)
    # merge consecutive single capital letter
    result = []
    buffer = ''
    for part in parts:
        # normal case
        if len(part) > 1:
            # clear last
            if buffer:
                result.append(buffer)
                buffer = ''
            result.append(part)
        else:
            buffer += part
    if buffer:
        result.append(buffer)

    return ['_'.join(part.lower() for part in result)]


class AppStarter(ABC):
    """
    Abstract application starter. Make a application by extending this class.

    Example:
        >>> class MyApp(AppStarter):
        >>>     scan_paths = ['package1']
        The class property scan_paths is needed to override in order to includes all the
        packages to be registered.

        After the configuration:
        >>> my_app = MyApp.config()
        You need to make the application, and run the server:
        >>> my_app.run()

    Args:
        fast_api (FastAPI): this path is automatically injected when calling the
            config function.
    """
    scan_paths: List[str] = []
    scan_base_dir: str = '.'
    graph_config = dict()

    origins = [
        "http://155.69.146.227",
        "http://155.69.146.227:3000",
    ]

    def __init__(self, fast_api: FastAPI):
        self.fast_api = fast_api
        self.fast_api.add_middleware(
            CORSMiddleware,
            allow_origins=AppStarter.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @classmethod
    def config(cls):
        """Make an instance of AppStarter using the overridden configurations.

        Returns:
            An instance of AppStarter
        """
        # before init hook
        cls.before_init()

        # scan for packages
        for path in cls.scan_paths:
            scan_package(path, cls.scan_base_dir)

        # build IoC graph
        global __context__
        __context__ = cls.__new_ioc_graph()

        # init all controllers
        for subclass in Controller.__subclasses__():
            __context__.provide(subclass)

        # after init hook
        cls.after_init()

        return __context__.provide(cls)

    def run(self):
        """Run the built application.
        """
        uvicorn.run(self.fast_api, host="0.0.0.0", port=8000)

    @classmethod
    def __new_ioc_graph(cls) -> pinject.object_graph.ObjectGraph:
        config = cls.graph_config
        arg_to_class = config.get('get_arg_names_from_class_name', get_arg_names_from_class_name)
        config['get_arg_names_from_class_name'] = arg_to_class
        return pinject.new_object_graph(**config)

    @classmethod
    def before_init(cls) -> None:
        """Before initialization hook
        """
        pass

    @classmethod
    def after_init(cls) -> None:
        """After initialization hook
        """
        pass
