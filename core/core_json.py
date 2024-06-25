import uuid
from typing import Dict

from django.http import HttpResponse
from orjson import orjson


# def default(obj):
#     if isinstance(obj, uuid.UUID):
#         return obj.hex


def dumps(*args, **kwargs) -> bytes:
    return orjson.dumps(*args, **kwargs)


def loads(*args, **kwargs) -> Dict:
    return orjson.loads(*args, **kwargs)


class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before ECMAScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be a json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    :param json_dumps_params: A dictionary of kwargs passed to json.dumps().
    """

    def __init__(
        self,
        data: Dict,
        json_dumps_params=None,
        **kwargs,
    ):
        if json_dumps_params is None:
            json_dumps_params = {}
        kwargs.setdefault("content_type", "application/json")
        data = dumps(data, **json_dumps_params)
        super().__init__(content=data, **kwargs)


