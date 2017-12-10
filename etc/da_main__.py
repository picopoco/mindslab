#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
#
#
# 1. 데이타가 들어오는 부분
#
#
# 2. 응답
#
# 3. lms 부분
#
# 4.평가 서버 연동 부분.
#
program = []
lecture = [1,2,3]
turn  = [1,2,3,4,5]

lectureOrder = ['open','sq','song','int','k1a','k1b','k1s','k2s','eq''end']

class front:
    def __init__(self):
        pass

    @staticmethod
    def getFront():
        return "front getFront"


class lms:
    def __init__(self):
        pass

    @staticmethod
    def lmsplay():
        t = front.getFront()
        print 'lmsplay ' ,t

        return 'return lmsplay'


class DaControl():

    def __init__(self,context):
        print 'DaContro init' ,self, context
        pass

    def process(param):
        print 'process', param
        start = lms.lmsplay()


if __name__ == '__main__':
    print "_main__"

    context  = '3강으로 이동 해줘'
    DaControl(context)
