'''An example OPC UA server which sets objects and variables for each IMMS'''

import sys
sys.path.insert(0, "..")
import time
import os
from opcua import ua, Server

NUMBER_OF_IMMS = int(os.environ.get("NUMBER_OF_IMMS", "1"))

if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    immss = []
    imms_dates = []
    imms_times = []
    imms_ActSimPara1s = []
    imms_ActSimPara2s = []
    imms_ActCntCycs = []
    imms_ActCntPrts = []
    imms_ActStsMachs = []
    imms_ActTimCycs = []
    imms_SetCntMlds = []
    imms_SetCntPrts = []
    imms_SetTimCycs = []
    imms_timestamps = []

    # populating our address space
    for i in range(NUMBER_OF_IMMS):
        imms = objects.add_object(idx, "IMMS_" + str(i + 1))
        immss.append(imms)

        imms_date = imms.add_variable(idx, "DATE", 0, varianttype=ua.VariantType.Double)
        imms_date.set_writable()
        imms_dates.append(imms_date)

        imms_time = imms.add_variable(idx, "TIME", "", varianttype=ua.VariantType.String)
        imms_time.set_writable()
        imms_times.append(imms_time)

        imms_ActSimPara1 = imms.add_variable(idx, "ActSimPara1", 0, varianttype=ua.VariantType.Double)
        imms_ActSimPara1.set_writable()
        imms_ActSimPara1s.append(imms_ActSimPara1)

        imms_ActSimPara2 = imms.add_variable(idx, "ActSimPara2", 0, varianttype=ua.VariantType.Double)
        imms_ActSimPara2.set_writable()
        imms_ActSimPara2s.append(imms_ActSimPara2)

        imms_ActCntCyc = imms.add_variable(idx, "ActCntCyc", 0, varianttype=ua.VariantType.Double)
        imms_ActCntCyc.set_writable()
        imms_ActCntCycs.append(imms_ActCntCyc)

        imms_ActCntPrt = imms.add_variable(idx, "ActCntPrt", 0, varianttype=ua.VariantType.Double)
        imms_ActCntPrt.set_writable()
        imms_ActCntPrts.append(imms_ActCntPrt)

        imms_ActStsMach = imms.add_variable(idx, "ActStsMach", "", varianttype=ua.VariantType.String)
        imms_ActStsMach.set_writable()
        imms_ActStsMachs.append(imms_ActStsMach)

        imms_ActTimCyc = imms.add_variable(idx, "ActTimCyc", 5, varianttype=ua.VariantType.Double)
        imms_ActTimCyc.set_writable()
        imms_ActTimCycs.append(imms_ActTimCyc)

        imms_SetCntMld = imms.add_variable(idx, "SetCntMld", 0, varianttype=ua.VariantType.Double)
        imms_SetCntMld.set_writable()
        imms_SetCntMlds.append(imms_SetCntMld)

        imms_SetCntPrt = imms.add_variable(idx, "SetCntPrt", 0, varianttype=ua.VariantType.Double)
        imms_SetCntPrt.set_writable()
        imms_SetCntPrts.append(imms_SetCntPrt)

        imms_SetTimCyc = imms.add_variable(idx, "SetTimCyc", 0, varianttype=ua.VariantType.Double)
        imms_SetTimCyc.set_writable()
        imms_SetTimCycs.append(imms_SetTimCyc)

    # starting!
    server.start()
