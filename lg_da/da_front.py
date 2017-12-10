#!/usr/bin/env python
# -*- coding: utf-8 -*-

class front:
    def __init__(self,context):
        print 'frontSample init', self ,context
        pass

    @classmethod
    def getFront(self):
        return {'lecture':3}

