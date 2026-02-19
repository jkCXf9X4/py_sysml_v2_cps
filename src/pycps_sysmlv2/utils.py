"""Helpers for normalizing SysML primitive type names."""

from __future__ import annotations

def obj_base(obj):
    if isinstance(obj, list) and obj:
        if len(obj) == 0:
            return None
        return obj_base(obj[0])
    return obj

def obj_iterator(values):
    if isinstance(values, (list, tuple)):
        for i in values:
            yield i
    else:
        yield values







