#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import grpc
import argparse

from concurrent import futures
import time

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + '/../lib/python')
sys.path.append(lib_path)
print bin_path

from google.protobuf import empty_pb2
from maum.brain.sds import sds_pb2
from maum.brain.sds import resolver_pb2


# from elsa.facade import userattr_pb2
# from maum.m2u.da import provider_pb2

#
# DIALOG METHODS
#


def serve():
    parser = argparse.ArgumentParser(description='dialInternalDB Test')
    parser.add_argument('-e', '--endpoint',
                        nargs='?',
                        dest='endpoint',
                        required=True,
                        type=str,
                        help='server to access SDS')

    args = parser.parse_args()

    sds_stub = sds_pb2.SpokenDialogServiceInternalStub(
        grpc.insecure_channel(args.endpoint))
    empty = empty_pb2.Empty()

    print "<Model List>"
    modelList = sds_stub.GetCurrentModels(empty)
    for ml in modelList.models:
        print str(ml)

    session_id = 1

    name = raw_input("Choose a domain: ")

    # Create DialogSessionKey & set session_key
    dp = sds_pb2.DialogueParam()
    dp.session_key = session_id
    dp.model = name

    # Dialog Open
    OpenResult = sds_stub.Open(dp)

    model = resolver_pb2.Model()
    model.name = name
    model.lang = 1
    model.is_external = False

    print(OpenResult.system_dialog)

    sdsUser = sds_pb2.SdsQuery()
    sdsUser.session_key = 1
    sdsUser.model = name
    user_utter = raw_input("[User]  ")
    sdsUser.utter = user_utter
    Dialog = sds_stub.Dialog(sdsUser)

    while (Dialog.status == "no end"):
        print Dialog

        print Dialog.response

        user_utter = raw_input("[User] ") + "\n"

        sdsUser.utter = user_utter

        Dialog = sds_stub.Dialog(sdsUser)

    print "You have successfully finished unit " + name + "!\n"

    dsk = sds_pb2.DialogueParam()
    dsk.session_key = 1
    dsk.model = name
    print dsk

    sds_stub.Close(dsk)

    print("SDS is now closed")


if __name__ == '__main__':
    serve()
