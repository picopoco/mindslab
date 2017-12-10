#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lms_client import lmsClient


from  da_front  import front

class daMain:
    def __init__(self):
        context = 'context'

        param = front.getFront()
        if  param :
            print 'getFront param2', param['lecture']
        response =  lmsClient.sendLmsData(param)
        print 'response' ,response
        pass


if __name__ == '__main__':
    print "_main__"
    daMain()

