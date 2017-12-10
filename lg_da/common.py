#!/usr/bin/env python
# -*- coding: utf-8 -*-

def deepupdate(original, update):

    for key, value in original.iteritems():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            deepupdate(value, update[key])
    return update

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r
