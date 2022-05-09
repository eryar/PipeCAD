# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :: Welcome to PipeCAD!                                      ::
# ::  ____                        ____     ______  ____       ::
# :: /\  _`\   __                /\  _`\  /\  _  \/\  _`\     ::
# :: \ \ \L\ \/\_\  _____      __\ \ \/\_\\ \ \L\ \ \ \/\ \   ::
# ::  \ \ ,__/\/\ \/\ '__`\  /'__`\ \ \/_/_\ \  __ \ \ \ \ \  ::
# ::   \ \ \/  \ \ \ \ \L\ \/\  __/\ \ \L\ \\ \ \/\ \ \ \_\ \ ::
# ::    \ \_\   \ \_\ \ ,__/\ \____\\ \____/ \ \_\ \_\ \____/ ::
# ::     \/_/    \/_/\ \ \/  \/____/ \/___/   \/_/\/_/\/___/  ::
# ::                  \ \_\                                   ::
# ::                   \/_/                                   ::
# ::                                                          ::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# PipeCAD - Piping Design Software.
# Copyright (C) 2021 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 11:20 2021-11-15

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


def ExportPcf(theTreeItem, theFileName):
    aPcfFile = open(theFileName, "w")

    # PCF HEADER
    aPcfFile.write("ISOGEN-FILES   ISOGEN.FLS")
    aPcfFile.write("\nUNITS-BORE   MM")
    aPcfFile.write("\nUNITS-CO-ORDS   MM")
    aPcfFile.write("\nUNITS-BOLT-LENGTH   MM")
    aPcfFile.write("\nUNITS-BOLT-DIA   MM")
    aPcfFile.write("\nUNITS-WEIGHT  KGS")

    # PIPELINE
    aPcfFile.write("\nPIPELINE-REFERENCE   " + theTreeItem.Name)
    aPcfFile.write("\n    PIPING-SPEC   ")
    aPcfFile.write("\n    INSULATION-SPEC   ")
    aPcfFile.write("\n    PAINTING-SPEC   ")
    aPcfFile.write("\n    TRACING-SPEC   ")

    # COMPONENT
    aBranchList = []
    if theTreeItem.Type == "PIPE":
        aBranchList = theTreeItem.Member
    elif theTreeItem.Type == "BRAN":
        aBranchList.append(theTreeItem)
    # if

    # Item Code Dict.
    aCodeDict = dict()

    for aBranItem in (aBranchList):
        aHeadPoint = aBranItem.Hposition
        aTailPoint = aBranItem.Tposition

        for aCompItem in aBranItem.Member:
            aType = aCompItem.FullType
            aArrivePoint = aCompItem.ArrivePoint
            aLeavePoint = aCompItem.LeavePoint

            try:
                aDetref = aCompItem.Spref.Detref
                aSkey = aDetref.Skey
                aCode = aDetref.Name
                aDescription = aCompItem.Dtxr
            except Exception as e:
                aSkey = ""
                aCode = ""
                aDescription = ""

            if aHeadPoint.distance(aArrivePoint.Position) > 1:
                # Add Pipe
                aPcfFile.write("\nPIPE")
                aPcfFile.write("\n    END-POINT    " + aHeadPoint.string() + " " + aArrivePoint.Bore)
                aPcfFile.write("\n    END-POINT    " + aArrivePoint.Position.string() + " " + aArrivePoint.Bore)
                aPcfFile.write("\n    PIPING-SPEC   ")
                aPcfFile.write("\n    INSULATION-SPEC   ")
                aPcfFile.write("\n    PAINTING-SPEC   ")
                aPcfFile.write("\n    TRACING-SPEC   ")
                aPcfFile.write("\n    WEIGHT   ")
                aPcfFile.write("\n    ITEM-CODE   PA100" )
                aPcfFile.write("\n    ITEM-DESCRIPTION   PIPE SCH80 ANSI B36.10")

            aHeadPoint = aLeavePoint.Position

            if aType.startswith("REDUCER"):
                if aSkey.startswith("RC"):
                    aType = "REDUCER-CONCENTRIC"
                else:
                    aType = "REDUCER-ECCENTRIC"

            aPcfFile.write("\n" + aType)
            aPcfFile.write("\n    END-POINT    " + aArrivePoint.Position.string() + " " + aArrivePoint.Bore + " " + aArrivePoint.Type)
            aPcfFile.write("\n    END-POINT    " + aLeavePoint.Position.string() + " " + aLeavePoint.Bore + " " + aLeavePoint.Type)

            if aType == "TEE":
                aBranchIndex = 6 - aCompItem.Arrive - aCompItem.Leave
                aBranchPoint = aCompItem.linkPoint("P" + str(aBranchIndex))
                aPcfFile.write("\n    CENTRE-POINT   " + aCompItem.Position.string())
                aPcfFile.write("\n    BRANCH1-POINT   " + aBranchPoint.Position.string() + " " + aBranchPoint.Bore + " " + aBranchPoint.Type)
            elif aType == "ELBOW":
                aPcfFile.write("\n    CENTRE-POINT   " + aCompItem.Position.string())


            aPcfFile.write("\n    SKEY     " + aSkey)
            aPcfFile.write("\n    PIPING-SPEC   ")
            aPcfFile.write("\n    INSULATION-SPEC   ")
            aPcfFile.write("\n    PAINTING-SPEC   ")
            aPcfFile.write("\n    TRACING-SPEC   ")
            aPcfFile.write("\n    WEIGHT   ")
            aPcfFile.write("\n    ITEM-CODE   " + aCode)
            aPcfFile.write("\n    ITEM-DESCRIPTION   " + aDescription)

            if len(aCode) > 0:
                aCodeDict[aCode] = aDescription
        # for

        # Add last pipe.
        if aHeadPoint.distance(aTailPoint) > 1:
            # Add Pipe
            aPcfFile.write("\nPIPE")
            aPcfFile.write("\n    END-POINT    " + aHeadPoint.string() + " " + aBranItem.Tbore)
            aPcfFile.write("\n    END-POINT    " + aTailPoint.string() + " " + aBranItem.Tbore)
            aPcfFile.write("\n    PIPING-SPEC   ")
            aPcfFile.write("\n    INSULATION-SPEC   ")
            aPcfFile.write("\n    PAINTING-SPEC   ")
            aPcfFile.write("\n    TRACING-SPEC   ")
            aPcfFile.write("\n    WEIGHT   ")
            aPcfFile.write("\n    ITEM-CODE   PA100")
            aPcfFile.write("\n    ITEM-DESCRIPTION   PIPE SCH80 ANSI B36.10")
    # for

    # ITEM-CODE
    aPcfFile.write("\nMATERIALS")
    aPcfFile.write("\nITEM-CODE    PA100")
    aPcfFile.write("\n    DESCRIPTION    PIPE SCH80 ANSI B36.10")
    for (aKey, aValue) in aCodeDict.items():
        aPcfFile.write("\nITEM-CODE    " + aKey)
        aPcfFile.write("\n    DESCRIPTION    " + aValue)
    # for

    aPcfFile.write("\n")
    aPcfFile.close()
# ExportPcf

