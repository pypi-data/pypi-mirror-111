# coding: utf-8
# Copyright (c) Qotto, 2021

"""
Eventy context
--------------

Provides wrappers around contextvars for correlation_id and request_id
"""

from contextvars import ContextVar, Token


class EventyContext:
    """
    Essentially a wrapper around contextvars.ContextVar
    """
    _contextvar: ContextVar

    def __init__(self, var_name: str):
        self._contextvar = ContextVar(var_name, default="")

    @property
    def name(self) -> str:
        """
        Name of the context variable

        :return: the name of the underlying ContextVar
        """
        return self._contextvar.name

    def get(self) -> str:
        """
        Current value of context id

        :return: the value in current execution context
        """
        return self._contextvar.get()

    def set(self, value: str) -> Token:
        """
        Set the value

        :param value: new value
        :return: token that can be used to reset to previous value
        """
        return self._contextvar.set(value)

    def is_defined(self) -> bool:
        """
        Test if value was set or is still the default value (empty string)

        :return: True if value is set, false otherwise
        """
        return self.get() != ''

    def unset(self) -> str:
        """
        Reset the value to the default value empty string)

        :return: the value before reset
        """
        previous = self.get()
        self._contextvar.set('')
        return previous

    def reset(self, token: Token) -> str:
        """
        Reset the value to a previous state

        :param token: token obtained with set()
        :return: the value before reset
        """
        previous = self.get()
        self._contextvar.reset(token)
        return previous


correlation_id_ctx = EventyContext("correlation_id")
"""
Correlation ID context

>>> from eventy.context import correlation_id_ctx
>>> correlation_id_ctx.set('my_operation_using_many_services')
"""

request_id_ctx = EventyContext("request_id")
"""
Request ID context

>>> from eventy.context import request_id_ctx
>>> request_id_ctx.set('my_service_request')
"""
