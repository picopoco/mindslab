#!/usr/bin/env python
#
# SDS Resolver
#

import unittest
import grpc
import sys
import os

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + '/../lib/python')
sys.path.append(lib_path)

from google.protobuf import empty_pb2
from maum.brain.sds import sds_pb2
from maum.brain.sds import resolver_pb2


class SDSResolverPrototype(object):
    '''
    : sds resolver prototype.
    '''

    ### local
    # sds_server_addr = '127.0.0.1'
    # sds_server_port = '9880'

    ### remote
    # sds_server_addr = '10.1.19.5'
    # sds_server_port = '9906'

    def __init__(self):
        # grpc channel
        self.channel = grpc.insecure_channel('0.0.0.0:9860')

        # resolver
        self.resolver = resolver_pb2.SdsServiceResolverStub(self.channel)

    def parse(self, param):
        o = sds_pb2.ServiceQuery()
        o.name = param['name']
        o.lang = param['lang']
        o.is_external = param['is_external']
        return o if o else None

    def find(self, param={}):
        query = self.parse(param)
        remote = self.resolver.Find(query)
        print '[debug] remote => %s' % remote.__str__()


class TestSDSResolver(unittest.TestCase):
    '''
    : unit test for sds resolver.
    '''

    resolver = SDSResolverPrototype()

    images = (os.environ['HOME'] or os.path.expanduser('~')) + \
             '/maum/trained/sds-group/test-%s'

    def test_empty(self):
        param = {
            'name': '',
            'lang': '',
            'is_external': ''}
        self.resolver.find(param)

    def test_kor_internal(self):
        param = {
            'name': 'AI_Agent',
            'lang': 'kor',
            'is_external': 'False'}
        pass

    def test_eng_internal(self):
        param = {
            'name': 'AI_Agent_Eng',
            'lang': 'eng',
        'is_external':'False'}
        pass

    def test_kor_external(self):
        # TODO
        param = {
            'name': 'AI_Agent',
            'lang': 'kor',
            'is_external':'True'}
        self.resolver.find(param)

    def test_eng_external(self):
        # TODO
        param = {
            'name': 'AI_Agent_Eng',
            'lang': 'eng',
            'is_external':'True'}
        self.resolver.find(param)


if __name__ == '__main__':

    test_suites = []
    test_cases = [
        TestSDSResolver
    ]

    for test_case in test_cases:
        test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        test_suites.append(test_suite)

    result = unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite(test_suites))
    sys.exit(not result.wasSuccessful())
