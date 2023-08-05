# coding: utf-8
# Copyright (c) Qotto, 2021

from .context_filters import add_trace_id_filter, add_request_id_filter
from .gke_handler import GkeHandler
from .simple_handler import SimpleHandler

__all__ = [
    'add_trace_id_filter',
    'add_request_id_filter',
    'SimpleHandler',
    'GkeHandler',
]


def getLogger(__name__):
    return None
