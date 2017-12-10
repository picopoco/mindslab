#! /usr/bin/env python
#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import grpc
import argparse

from concurrent import futures
import time
import grpc


exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + '/../lib/python')
sys.path.append(lib_path)
print bin_path

from google.protobuf import empty_pb2
from maum.brain.sds import resolver_pb2
from maum.brain.sds import sds_pb2

#
# DIALOG METHODS
#


def serve():
    sds_channel = grpc.insecure_channel('0.0.0.0:9860')
    resolver_stub = resolver_pb2.SdsServiceResolverStub(sds_channel)
    #print sds_channel

    print 'resolver_stub', resolver_stub

        
    MG = resolver_pb2.ModelGroup()
    MG.name = 'test_kor'
    MG.lang = 0
    MG.is_external = True
    print MG

    resolver_stub.CreateModelGroup(MG)

    M = resolver_pb2.Model()
    M.lang = 0
    M.is_external = True
    
    MP = resolver_pb2.ModelParam()
    MP.lang = 0
    MP.group_name = 'test_kor'
    MP.is_external = True


    print MP

    ML = resolver_pb2.ModelList()

    model_name_list = ['base', 'AI_Agent']

    for mn in model_name_list:
        M.name = mn
        MP.model_name = mn

        M = ML.models.add()
        resolver_stub.LinkModel(MP)
        
    ss = resolver_stub.Find(MG)
    print ss

    sds_stub = sds_pb2.SpokenDialogServiceStub(
        grpc.insecure_channel(ss.server_address))

    print sds_stub
    time.sleep(20)

    
    empty = empty_pb2.Empty()

    time.sleep(20)
    cML = sds_stub.GetCurrentModels(empty)
    print 'cML'
    print cML
    aML = sds_stub.GetAvailableModels(empty)
    print 'aML'
    print aML
    pong = sds_stub.Ping(MG)
    print pong
    
    dp = sds_pb2.DialogueParam()
    dp.model = 'AI_Agent'
    dp.session_key = 0
    dp.user_initiative = False


    OpenResult = sds_stub.Open(dp)

    print OpenResult


    sq = sds_pb2.SdsQuery()
    sq.model = dp.model
    sq.session_key = dp.session_key
    sq.apply_indri_score = 0
    sq.utter = '안녕'
    
    Intent = sds_stub.Understand(sq)

    print Intent


    Entity = sds_pb2.Entities()
    Entity.session_key = dp.session_key
    Entity.model = dp.model

    sds_utter = sds_stub.GenerateEntities(Entity)
    print sds_utter

    print sds_utter.response
    
    '''
    cML = sds_stub.GetAvailableModels(empty)
    print cML
    
    ML3 = sds_stub.GetCurrentModels(empty)
    print 'ML3', ML3
    
    ML4 = sds_stub.GetAvailableModel(empty)
    print 'ML4', ML4
    
    
    sds_stub.AddModel(M1)
    ML3 = sds_stub.GetCurrentModels(empty)
    print 'ML3', ML3
    
    ML4 = sds_stub.GetAvailableModel(empty)
    print 'ML4', ML4

    sds_stub.RemoveModel(M1)
    ML3 = sds_stub.GetCurrentModels(empty)
    print 'ML3', ML3



    

    ML5 = sds_stub2.GetCurrentModels(empty)
    print 'ML5', ML5
    
    ML6 = sds_stub2.GetAvailableModel(empty)
    print 'ML6', ML6

    sds_stub2.AddModel(M3)
    ML5 = sds_stub.GetCurrentModels(empty)
    print 'ML5', ML5
    
    ML6 = sds_stub.GetAvailableModel(empty)
    print 'ML6', ML6
    
    sds_stub2.RemoveModel(M3)
    ML5 = sds_stub.GetCurrentModels(empty)
    print 'ML5', ML5
    
    

    
    
    
    sdsmodel = sds_pb2.Model()
    sdsmodel.path = "test-eng"
    sdsmodel.lang = 1
    sdsmodel.is_external = False


    sdsmodel2 = sds_pb2.Model()
    sdsmodel2.path = "test_eng_20170817"
    sdsmodel2.lang = 1
    sdsmodel2.is_external = False


    print "serverstatus 1"
    empty = empty_pb2.Empty()
    server_status = resolver_stub.Find(sdsmodel)
    
    print server_status

    print "serverstatus 2"

    server_status2 = resolver_stub.Find(sdsmodel2)

    print server_status2


    print "serverstatus 3"

    server_status3 = resolver_stub.Ping(sdsmodel)

    print server_status3


    print "serverstatus 4"

    server_status4 = resolver_stub.Stop(sdsmodel)
    print server_status4

    print "serverstatus 5"
    server_status5 = resolver_stub.Restart(sdsmodel2)
    print server_status5

    
    sds_stub = sds_pb2.SpokenDialogServiceInternalStub(grpc.insecure_channel(server_status.server_address))

    
    empty = empty_pb2.Empty()
    print "<Domain List>"

    #domainList = sds_stub.GetDomainList(empty)

    #for dl in domainList.domains:
    #    print str(dl)

    #session_id = 1

    name = raw_input("Choose a domain: " )

    # Create DialogSessionKey & set session_key
    DialogueParam = sds_pb2.DialogueParam()
    DialogueParam.session_key = 1111
    DialogueParam.domain = name


    # Dialog Open
    OpenResult = sds_stub.Open(DialogueParam)
    #model = sds_pb2.Model()

    
    #serverstat = sds_stub.Ping(model)
    #print "lang is " + str(serverstat.lang)
    #print "model is " + serverstat.model
    #print "state is " + str(serverstat.state)
    #print "server address is " + serverstat.server_address
    #print "invoked by is " + serverstat.invoked_by

    #isdomainin = sds_stub.IsInDomainList(model)
    #print isdomainin.status()


    print(OpenResult.system_dialog)

    sdsUser = sds_pb2.SdsQuery()
    sdsUser.session_key = 1
    user_utter =raw_input("[User]  ")
    sdsUser.utter = user_utter
    Dialog = sds_stub.Dialog(sdsUser)


    while (Dialog.status == "no end"):
        
        print Dialog

        print Dialog.response
      
        user_utter = raw_input("[User] ") + "\n"

        sdsUser.utter = user_utter
        
        Dialog = sds_stub.Dialog(sdsUser) 

    

    print "You have successfully finished unit " + name + "!\n"  

    dsk = sds_pb2.DialogueSessionKey()
    dsk.session_key = 1
    print dsk
    
    sds_stub.Close(dsk)

    print("SDS is now closed")
    '''

    
if __name__ == '__main__':
    serve()

