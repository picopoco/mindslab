#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  da_front  import front
import simplejson, urllib


class lmsClient:
    def __init__(self,context):
        context = 'context'
    pass

    @classmethod
    def sendLmsData(self,param):
        print 'sendLmsDataRest'
        apikey = "DAUM_SEARCH_DEMO_APIKEY"
        SEARCH_BASE = "http://127.0.0.1:5000"

        def search(query, **args):
            args.update({
                'apikey': apikey,
                'q': query,
                'output': 'json'
            })

       # url = SEARCH_BASE + '?' + urllib.urlencode(args)
        url =  SEARCH_BASE
        print 'url', url
        result = simplejson.load(urllib.urlopen(url))
        print result
        return result
        # return result['cur_turn']
        # info = search('OpenAPI')
        # for item in info['item']:
        #  print item['cur_turn']




if __name__ == '__main__':
    print "lmsClient"
    lmsClient()

