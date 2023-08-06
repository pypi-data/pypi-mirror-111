# coding: utf-8
# Copyright (c) Qotto, 2021

"""
Common integration utilities
----------------------------

Utility functions to integrate the eventy protocol in your workflow

Provides decorator factories to decorate functions and automatically extract context information
"""

import logging
from base64 import b64encode
from datetime import datetime, timezone
from secrets import token_urlsafe
from typing import Callable

from ..context import EventyContext

logger = logging.getLogger(__name__)

__all__ = [
    'with_context',
    'merge_decorators',
    'DecoratorType',
    'generate_simple_id',
    'simple_func_id_generator',
]

DecoratorType = Callable[..., Callable]


def merge_decorators(
    *decorators,
) -> DecoratorType:
    """
    Decorator factory merging multiple decorators, apply from left to right

    :param decorators: decorators to merge
    :return: a new decorator applying all decorators
    """

    if not decorators:
        def identity(func):
            return func

        return identity

    def decorator(func):
        def decorated_func(*args, **kwargs):
            inner_func = func
            nested_decorators = decorators
            for nested_decorator in nested_decorators:
                inner_func = nested_decorator(inner_func)

            return inner_func(*args, **kwargs)

        return decorated_func

    return decorator


def with_context(
    context: EventyContext,
    generator: Callable[[Callable, tuple, dict], str],
    reset: bool = True,
    fetch: bool = True,
    override_context: bool = False,
) -> DecoratorType:
    """
    Decorator factory fetching context id from kwargs

    :param context: correlation_id_ctx or request_id_ctx
    :param generator: function to generate context id,
            args are: decorated function, ``*args`` and ``**kwargs`` of function call
    :param reset: should the context id be reset after function call?
    :param fetch: should the context id be fetched from decorated function kwargs?
    :param override_context: should the new context override existing context?
    :return: A decorator
    """

    def decorator(func):
        def decorated_func(*args, **kwargs):
            token = None
            if context.name in kwargs and fetch:
                context_id = kwargs.pop(context.name)

                if override_context or not context.is_defined():
                    logger.debug(f'Will set {context.name}={context_id} from {func.__name__} kwargs')
                    token = context.set(context_id)

                else:
                    logger.debug(f'Will not use {context.name}={context_id} from {func.__name__} kwargs')

            elif generator:
                context_id = generator(func, *args, **kwargs)

                if override_context or not context.is_defined():
                    logger.debug(f'Will set {context.name}={context_id} generated for {func.__name__}')
                    token = context.set(context_id)

                else:
                    logger.debug(f'Will not use {context.name}={context_id} generated for {func.__name__}')

            result = func(*args, **kwargs)

            if token and reset:
                prev = context.reset(token)
                logger.debug(f'Reset {context.name} for {func.__name__} (was: {prev})')

            return result

        renamed_decorated_func = decorated_func
        renamed_decorated_func.__name__ = func.__name__
        return renamed_decorated_func

    return decorator


def generate_simple_id(
    prefix: str,
    content: str,
):
    """
    Create a context id string as "prefix:content:encoded_date:random"

    :param prefix: prefix part
    :param content: content part
    :return:
    """
    ts_now = datetime.now(timezone.utc).timestamp()
    ts_2k = datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp()
    ts2000res65536 = int(65536 * (ts_now - ts_2k)).to_bytes(6, 'big')
    date = b64encode(ts2000res65536, b'_-').decode('ascii')
    random = token_urlsafe(3)
    id = f'{prefix}:{content}:{date}:{random}'
    logger.debug(f'Generated context id: {id}')
    return id


def simple_func_id_generator(
    namespace: str = '-',
):
    """
    Context id generator factory, using namespace as prefix and function.__name__ as content

    Can then be used as::

        id_generator(func: Callable, *args, **kwargs) -> str:

    Example::

        gen = simple_func_id_generator('my_service')
        def my_task():
            pass
        gen(my_task) # -> "my_service:my_task:KG9MGaVh:NE4y"

    :param namespace: used as prefix in context id
    :return: context id generator
    """

    def id_generator(func: Callable, *args, **kwargs) -> str:
        return generate_simple_id(namespace, func.__name__)

    return id_generator
