import inspect
import os.path as osp
from abc import ABC
from datetime import datetime
from typing import Any, Callable, Dict, List, Sequence, Set, Type, Union

from fastapi import FastAPI
from fastapi.params import Depends
from starlette.responses import Response, JSONResponse


class Controller(ABC):
    """
    Abstract controller. All controller has to be extended from this class so that
    the annotated mapping can take effect. A controller is a place for routing
    configuration. By decorated with @mapping(...), the routing is automatically
    configured during the configuration stage of your Application which extends
    from AppStarter.
    """

    def __init__(self, fast_api: FastAPI, base_url: str = '/'):
        self.base_url = base_url
        self.fast_api = fast_api
        mappings = inspect.getmembers(self, predicate=lambda method: (
                inspect.ismethod(method) and getattr(method, '__mapping__', False)
        ))
        for _, method in mappings:
            path = osp.join(self.base_url, getattr(method, '__path'))
            kwargs = getattr(method, '__kwargs')
            fast_api.add_api_route(path, method, **kwargs)


def mapping(
        path: str,
        *,
        methods: List[str] = None,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Set[str] = None,
        response_model_exclude: Set[str] = None,
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
) -> Callable:
    """Decorator for setting the route with the function as a endpoint callback.
    """
    if response_model_exclude is None:
        response_model_exclude = set()

    def decorator(func2: Callable):
        kwargs = {
            'methods': methods,
            'response_model': response_model,
            'status_code': status_code,
            'tags': tags,
            'dependencies': dependencies,
            'summary': summary,
            'description': description,
            'response_description': response_description,
            'responses': responses,
            'deprecated': deprecated,
            'operation_id': operation_id,
            'response_model_include': response_model_include,
            'response_model_exclude': response_model_exclude,
            'response_model_by_alias': response_model_by_alias,
            'response_model_skip_defaults': response_model_skip_defaults,
            'include_in_schema': include_in_schema,
            'response_class': response_class,
            'name': name
        }
        setattr(func2, '__mapping__', True)
        setattr(func2, '__path', path)
        setattr(func2, '__kwargs', kwargs)
        return func2

    return decorator


def json_wrapper(data, status_code: int = 200, message: str = ''):
    result = dict()
    result['timestamp'] = datetime.now().timestamp()
    result['statusCode'] = status_code
    result['message'] = message
    result['data'] = data
    return result
