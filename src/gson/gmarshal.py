import importlib
import inspect
import json
import logging
from typing import (
    Any,
    Dict,
    ForwardRef,
    List,
    Tuple,
    Type,
    TypeVar,
    get_args,
    get_origin,
)

from decorators.safe_run import safe_run

logger = logging.getLogger(__name__)


def loads(input: str) -> Dict:
    """same as json.loads, no exception throws, only return empty dict on exception
    Args:
        input (str): [description]
    Returns:
        dict: [description]
    """
    res, err = _load(input)
    if err is not None or not isinstance(res, dict):
        return {}

    return res


@safe_run(logger=logger)
def _load(input: str):
    return json.loads(input)


def marshal(obj, omit_empty=True) -> str:
    """Attemp to convert any object to json str, no exceptions throws if failed

    Args:
        obj ([type]): anything
        omit_empty (bool, optional): ignore empty fields

    Returns:
        str: json string
    """
    return json.dumps(obj_to_dict(obj, omit_empty=omit_empty))


def obj_to_dict(obj, omit_empty=True):
    """Convert any object to dict. You can customize how one class should be converted to dict by
    implement object_to_dict method under the class
    def object_to_dict() -> dict

    Args:
        obj ([type]): [description]
        omit_empty (bool, optional): ignore empty fields. Defaults to True.

    Returns:
        json dict
    """
    if isinstance(obj, dict):
        res = {}
        for k in obj.keys():
            if not is_empty(obj[k]) or not omit_empty:
                res[k] = obj_to_dict(obj[k])
        return res
    elif getattr(obj, "obj_to_dict", None):
        return obj.obj_to_dict()
    elif hasattr(obj, "__dict__"):
        res = {}
        for k in obj.__dict__.keys():
            if not is_empty(obj.__dict__[k]) or not omit_empty:
                res[k] = obj_to_dict(obj.__dict__[k])
        return res
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        res = []
        for x in obj:
            if not is_empty(x) or not omit_empty:
                res.append(obj_to_dict(x))
        return res
    else:
        return obj


def is_empty(obj):
    if obj == {} or obj is None:
        return True
    return False


def to_legal_json_key(input: str) -> str:
    """
    convert my-info to my_info, since - is not legal json key

    Returns:
        str: converted key
    """
    if type(input) == str:
        return input.replace("-", "_")
    return input


def process_dict_key_to_be_legal(some_json: Dict[str, Any]):
    if not type(some_json) == dict:
        return
    for k in list(some_json.keys()):
        legal_k = to_legal_json_key(k)
        if legal_k != k:
            some_json[legal_k] = some_json[k]
            del some_json[k]
    for k in list(some_json.keys()):
        process_dict_key_to_be_legal(some_json[k])


@safe_run(logger=logger)
def _unmarshal(
    some_json: Dict[str, Any],
    some_cls: Type,
    ref_cls_module: str = "",
    keys: List[str] = [],
):
    """
    Construct instance of given type from json dict. Allowed class variable includes:
    1. primitive
    2. list tuple set
    3. another allowed class
    This is done by analyzing __init__ function of given class. You must write type hints for each function args
    you want to read from the dict. Giving no default value to an argument will cause reflection failure if the
    key doesn't exists in dict


    Args:
        some_json (dict): json dict
        some_cls ([type]): target class type
        cls_cache (dict, optional): class_name -> class itself, usally not necessary

    Returns:
        (obj, exception)
    """
    nested_cls = get_origin(some_cls)
    if nested_cls in (list, tuple, set):
        if not isinstance(some_json, list):
            return None
        else:
            if nested_cls == list:
                o = []
            elif nested_cls == tuple:
                o = ()
            elif nested_cls == set:
                o = set()
            for i, obj in enumerate(some_json):
                the_type = get_args(some_cls)[0]  # list[t1]
                if nested_cls == tuple:  # tuple[t1, t2, t3]
                    if i >= len(get_args(some_cls)):
                        the_type = type(obj)
                    the_type = get_args(some_cls)[i]
                cur_ref_cls_module = ref_cls_module
                if not cur_ref_cls_module and inspect.isclass(some_cls):
                    cur_ref_cls_module = some_cls.__module__
                res, _ = _unmarshal(obj, the_type, cur_ref_cls_module, keys)
                if res:
                    if nested_cls == list:
                        o.append(res)
                    elif nested_cls == tuple:
                        o = (res,)
                    elif nested_cls == set:
                        o.add(res)
            return o

    if nested_cls == dict:
        if not isinstance(some_json, dict):
            return None
        key_type, val_type = get_args(some_cls)  # Dict[key_type, val_type]
        if key_type != str:  # key must be str to be a legal json
            return None

        o = {}
        for k in some_json.keys():
            if not isinstance(k, str):
                continue
            res, _ = _unmarshal(some_json.get(k), val_type, ref_cls_module, keys + [k])
            if res:
                o[k] = res
        return o

    if nested_cls is not None:
        raise Exception(f"{nested_cls} is not supported!")

    some_cls = to_real_class(ref_cls_module, some_cls)
    if isinstance(some_json, dict) and inspect.isclass(some_cls):
        kwargs = {}

        annotations = {}
        annotations = some_cls.__init__.__annotations__
        if not annotations:
            annotations = (
                some_cls.__init__._sa_original_init.__annotations__
            )  # For sqlalchemy
        for field in annotations.keys():
            target_cls = annotations[field]
            if some_json.get(field) is None:
                continue

            if target_cls == type(some_json.get(field)):
                kwargs[field] = some_json.get(field)
            else:
                res, _ = _unmarshal(
                    some_json.get(field),
                    target_cls,
                    some_cls.__module__,
                    keys + [field],
                )
                if res:
                    kwargs[field] = res

        try:
            res = some_cls(**kwargs)
            return res
        except Exception as e:
            logger.exception(e, f"Field Stack: {keys}")
            return None

    if isinstance(some_json, (int, bool, float, str)):
        if some_cls == type(some_json):
            return some_json
        elif some_cls == int and isinstance(some_json, str):
            try:
                return int(some_json)
            finally:
                pass
        elif some_cls == bool:
            if isinstance(some_json, str):
                if some_json.lower() == "true":
                    return True
                elif some_json.lower() == "false":
                    return False
            return bool(some_json)
        else:
            logger.warning(f"Type miss match, field stack: {keys}")
    return None


T = TypeVar("T")


def unmarshal(json_input: Dict[str, Any], cls: Type[T]) -> Tuple[T, Exception]:
    process_dict_key_to_be_legal(json_input)
    res, e = _unmarshal(json_input, cls)
    return res, e


def unmarshal_from_str(str_input: str, cls: Type[T]) -> Tuple[T, Exception]:
    json_input, e = _load(str_input)
    if e:
        return None, e
    return unmarshal(json_input, cls)


def get_class(module_name: str, class_name: str) -> Type:
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def to_real_class(current_module, cls) -> Type:
    if isinstance(cls, str):
        return get_class(current_module, cls)
    elif isinstance(cls, ForwardRef):
        return get_class(current_module, cls.__forward_arg__)
    return cls
