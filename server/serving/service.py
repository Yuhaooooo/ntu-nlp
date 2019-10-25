import inspect
from typing import Callable, List, Tuple


class BaseService(object):
    def __init__(self):
        self._service_name = self.__class__.__name__
        self.__scan_procedures()

    @property
    def name(self):
        return self._service_name

    def __scan_procedures(self):
        self._procedures: List[Tuple[str, ProcedureDecorator]] = inspect.getmembers(
            self.__class__,
            predicate=lambda x: isinstance(x, ProcedureDecorator)
        )
        # inject service instance
        for _, procedure in self._procedures:
            setattr(procedure, '_instance', self)


class ProcedureDecorator:
    def __init__(self, func: Callable):
        assert callable(func), "@procedure cannot be decorated on a non-callable object"

        self._instance = None
        self._func = func

        self._dummy_processor = lambda _, x: x
        self._preprocessor = self._dummy_processor
        self._postprocessor = self._dummy_processor
        self._handler = self._dummy_processor

    def __call__(self, *args, **kwargs):
        return self._postprocessor(
            self._instance,
            self._func(
                self._instance,
                self._preprocessor(self._instance, *args, **kwargs)
            )
        )

    def preprocessor(self, func):
        assert self._dummy_processor is self._preprocessor, "One procedure call cannot have more than one preprocessors"
        self._preprocessor = func
        return func

    def postprocessor(self, func):
        assert self._dummy_processor is self._postprocessor, "One procedure call cannot have more than one " \
                                                             "postprocessors"
        self._postprocessor = func
        return func
