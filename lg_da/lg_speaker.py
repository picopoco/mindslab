#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from concurrent import futures
import time
import argparse
import grpc
from google.protobuf import empty_pb2
# import pymysql
import os
import re

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + '/../lib/python')
sys.path.append(lib_path)

from elsa.facade import userattr_pb2
from maum.m2u.da import provider_pb2
from maum.m2u.da.v1 import talk_pb2
from maum.brain.sds import sds_pb2
from maum.brain.sds import resolver_pb2
import logging

logging.basicConfig(filename='/home/kbs/maum/logs/pat.log', level=logging.DEBUG)
# import MySQLdb.cursors

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_REQ_REX_LG_SPEAKER = '^(\d+)_(\d)$'

class Stat:
    c_model = '001_1'

    def __init__(self):
        pass


class testDA(provider_pb2.DialogAgentProviderServicer):
    # STATE
    state = provider_pb2.DIAG_STATE_IDLE
    # provider_pb2.
    init_param = provider_pb2.InitParameter()

    # PROVIDER
    provider = provider_pb2.DialogAgentProviderParam()
    provider.name = 'testDA'
    provider.description = 'lg_speaker'
    provider.version = '0.1'
    provider.single_turn = False
    provider.agent_kind = provider_pb2.AGENT_SDS
    provider.require_user_privacy = True

    # PARAMETER
    sds_path = ''
    ''''
    sds_domain = ''
    db_host = ''
    db_port = 0
    db_user = ''
    db_pwd = ''
    db_database = ''
    db_table = ''
    loc_timediff = '0'
    '''
    # SDS Stub
    sds_server_addr = ''
    sds_stub = None
    server_status = None
    lang = 1  # ATTENTION - three lines
    is_external = False
    stat = {}
    model_list = ['001_1', '001_2', '002_1',  '003_1', '003_2', ]
    turn_match = {'1':'s','2':'e'}
    lecture_turn = '001_1'
    lecture = '001'
    turn = '1'
    def __init__(self):
        self.state = provider_pb2.DIAG_STATE_IDLE

    #
    # INIT or TERM METHODS
    #
    def get_sds_server(self):
        sds_channel = grpc.insecure_channel('localhost:9860')
        print 'stub'

        MG = resolver_pb2.ModelGroup()  # ATTENTION - Until Find Function
        MG.name = 'lg_speaker'
        MG.lang = self.lang
        MG.is_external = self.is_external

        resolver_stub = resolver_pb2.SdsServiceResolverStub(sds_channel)
        resolver_stub.CreateModelGroup(MG)

        MP = resolver_pb2.ModelParam()
        MP.lang = self.lang
        MP.is_external = self.is_external
        MP.group_name = MG.name

        for mn in self.model_list:
            MP.model_name = mn
            resolver_stub.LinkModel(MP)
            print "model_name : " + MP.model_name

        self.server_status = resolver_stub.Find(MG)
        logging.debug('find result :%s', self.server_status)

        self.sds_stub = sds_pb2.SpokenDialogServiceInternalStub(
            grpc.insecure_channel(self.server_status.server_address))
        self.sds_server_addr = self.server_status.server_address

    def IsReady(self, empty, context):
        print 'IsReady', 'called'
        status = provider_pb2.DialogAgentStatus()
        status.state = self.state
        return status

    def Init(self, init_param, context):
        print 'Init', 'called'
        self.state = provider_pb2.DIAG_STATE_INITIALIZING
        # COPY ALL
        self.init_param.CopyFrom(init_param)
        # DIRECT METHOD
        self.sds_path = init_param.params['sds_path']
        print 'path'

        self.get_sds_server()
        print 'sds called'
        self.state = provider_pb2.DIAG_STATE_RUNNING
        # returns provider
        result = provider_pb2.DialogAgentProviderParam()
        result.CopyFrom(self.provider)
        print 'result called'
        return result

    def Terminate(self, empty, context):
        print 'Terminate', 'called'
        # DO NOTHING
        self.state = provider_pb2.DIAG_STATE_TERMINATED
        return empty_pb2.Empty()

    #
    # PROPERTY METHODS
    #

    def GetProviderParameter(self, empty, context):
        print 'GetProviderParameter', 'called'
        result = provider_pb2.DialogAgentProviderParam()
        result.CopyFrom(self.provider)
        return result

    def GetRuntimeParameters(self, empty, context):
        print 'GetRuntimeParameters', 'called'
        params = []
        result = provider_pb2.RuntimeParameterList()
        print result
        sds_path = provider_pb2.RuntimeParameter()
        sds_path.name = 'sds_path'
        sds_path.type = userattr_pb2.DATA_TYPE_STRING
        sds_path.desc = 'DM Path'
        sds_path.default_value = '001_1'
        sds_path.required = True
        params.append(sds_path)

        result.params.extend(params)
        return result

    #
    # DIALOG METHODS
    #

    def Talk(self, talk, context):
        session_id = talk.session_id
        empty = empty_pb2.Empty()
        if not session_id in self.stat:
            self.stat[session_id] = Stat()
        local_stat = self.stat[session_id]

        logging.debug('target server address: %s', self.server_status.server_address)
        ## Opening AI_Manager_Start
        dp = sds_pb2.DialogueParam()
        dp.session_key = int(session_id)
        logging.debug('session : %d', dp.session_key)
        print  dp.session_key, 'talk.text: ', talk.text

	#print talk.text.find('lg_speaker_1_4_')
        p = re.compile(_REQ_REX_LG_SPEAKER)
        dp.model = str(talk.text)
        m = p.match(talk.text)
        if m:
          self.lecture_turn = m.group(0)
          self.lecture = m.group(1)
          self.turn = m.group(2)
          if self.lecture_turn in self.model_list:
            local_stat.c_model = self.lecture_turn
 
        dp.model = local_stat.c_model

        print 'dp model : ', dp.model
        logging.debug(dp) 

        OpenResult = self.sds_stub.Open(dp)
        logging.debug('Open result : %s', OpenResult)
        print 'openResult',OpenResult
        talk_res = provider_pb2.TalkResponse()

        if talk.text.lower() in ['end.', 'stop.', 'done.', 'skip.', 'before', 'next','one lecture','two lecture','tree lecture']:
            self.sds_stub.Close(dp)
            talk_res.text = "We are ending the service now. Bye"  # 문구 바꾸기
            print 'talk_res.text', talk_res.text ,talk.text.lower() 
            talk_res.state = provider_pb2.DIAG_CLOSED
            return talk_res

        sq = sds_pb2.SdsQuery()
        sq.session_key = dp.session_key
        sq.model = dp.model
        sq.utter = talk.text.lower()
        sq.apply_indri_score = 0

        Dialog = self.sds_stub.Dialog(sq)
        logging.debug('User_talk : %s', talk.text)
        logging.debug('Dialog : %s', Dialog)
        talk_res = provider_pb2.TalkResponse()
        talk_res.text = Dialog.response
        print 'talk_res.text', talk_res.text
        print 'Dialog.status',Dialog.status
        if Dialog.status == 'end':  # 한 session 마무리 시 다음 session으로 이동
            self.sds_stub.Close(dp)
            print "domain is closed"
            print 'self.turn_match',self.turn_match ,'turn', self.turn 
            print 'tm', self.turn_match[self.turn]
            talk_res.text = self.lecture + self.turn_match[self.turn] + "qga"
            talk_res.state = provider_pb2.DIAG_CLOSED
        else:
             talk_res.text = self.lecture + self.turn_match[self.turn] + "qwa"
        return talk_res

    def Close(self, req, context):
        print 'Closing for ', req.session_id, req.agent_key
        talk_stat = provider_pb2.TalkStat()
        talk_stat.session_key = req.session_id
        talk_stat.agent_key = req.agent_key
        dp = sds_pb2.DialogueParam()
        dp.session_key = req.session_id
        self.sds_stub.Close(dp)
        return talk_stat


def serve():
    parser = argparse.ArgumentParser(description='Test DA for English Education service')
    parser.add_argument('-p', '--port',
                        nargs='?',
                        dest='port',
                        required=True,
                        type=int,
                        help='port to access server')
    args = parser.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    provider_pb2.add_DialogAgentProviderServicer_to_server(
        testDA(), server)

    listen = '[::]' + ':' + str(args.port)
    server.add_insecure_port(listen)

    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
