#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import grpc
import argparse

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + '/../lib/python')
sys.path.append(lib_path)

from google.protobuf import empty_pb2
from maum.brain.sds import sds_pb2
from maum.brain.sds import resolver_pb2


#
# DIALOG METHODS
#
def serve():
    parser = argparse.ArgumentParser(description='dialExternalDB Test')
    parser.add_argument('-e', '--endpoint',
                        nargs='?',
                        dest='endpoint',
                        required=True,
                        type=str,
                        help='server to access SDS')
    args = parser.parse_args()

    sds_stub = sds_pb2.SpokenDialogServiceStub(
        grpc.insecure_channel(args.endpoint))
    empty = empty_pb2.Empty()

    print "<Model List>"
    modelList = sds_stub.GetCurrentModels(empty)
    for ml in modelList.models:
        print str(ml)

    print "select model"
    model = raw_input()

    session_id = 1
    print "Session ID : " + str(session_id)
    print "Model : " + str(model)

    # Create OpenParam & set session_key
    dp = sds_pb2.DialogueParam()
    dp.session_key = session_id
    dp.model = model

    # Dialog Open
    sdsSession = sds_stub.Open(dp)
    print "open success"

    sdsUser = sds_pb2.SdsQuery()
    sdsUser.session_key = 1
    sdsUser.model = model
    print("Hello!")

    user_utter = "hi"
    while (user_utter != "exit"):

        sdsUser.utter = user_utter
        sa = sds_stub.Understand(sdsUser)

        entities = sds_pb2.Entities()
        entities.session_key = 1
        entities.model = model
        sdsResponse = sds_stub.GenerateEntities(entities)

        if (not sdsResponse.response):
            break

        print "[System] " + sdsResponse.response

        user_utter = raw_input("[User]  ")

    sds_stub.Close(dp)

    print("SDS is closed")


if __name__ == '__main__':
    serve()
