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
# Copyright (C) 2022 Wuhan OCADE IT. Co., Ltd.
# Author: Shing Liu(eryar@163.com)
# Date: 21:20 2022-04-08

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *

import time


def exportParam(thePmlFile, theKey, theValue):
    if len(theValue) < 1:
        return
    # if

    if theValue.startswith("DD"):
        aSplits = theValue.split("*")
        if len(aSplits) > 1:
            thePmlFile.write("\n%s %s TIMES %s" % (theKey, aSplits[1], aSplits[0]))
        else:
            thePmlFile.write("\n%s %s" % (theKey, theValue))
        #if
    else:
        thePmlFile.write("\n%s (%s)" % (theKey, theValue))
    # if

# exportParam

def exportCatalogue(theTreeItem, thePmlFile):
    if theTreeItem is None:
        return
    # if

    if theTreeItem.Type == "CATA":
        # CATA
        exportCata(theTreeItem, thePmlFile)
    # if

# exportCatalogue

def exportCata(theTreeItem, thePmlFile):

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW CATALOGUE /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW CATALOGUE")
    # if

    if len(theTreeItem.Purpose) > 0:
        thePmlFile.write("\nPURP %s" % theTreeItem.Purpose)
    # if

    for aSectItem in theTreeItem.Member:
        exportSect(aSectItem, thePmlFile)
    # for

# exportCata

def exportSect(theTreeItem, thePmlFile):
    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SECTION /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SECTION")
    # if
    
    if len(theTreeItem.Purpose) > 0:
        thePmlFile.write("\nPURP %s" % theTreeItem.Purpose)
    # if

    for aCateItem in theTreeItem.Member:
        exportCate(aCateItem, thePmlFile)
    # for
# exportSect

def exportCate(theTreeItem, thePmlFile):
    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW CATEGORY /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW CATEGORY")
    # if

    if len(theTreeItem.Purpose) > 0:
        thePmlFile.write("\nPURP %s" % theTreeItem.Purpose)
    # if

    thePmlFile.write("\nDESC |%s|" % theTreeItem.Description)
    thePmlFile.write("\nGTYP %s" % theTreeItem.Gtype)
    thePmlFile.write("\n!aCategory = ce")
    thePmlFile.write("\n!aPtref = nulref")
    thePmlFile.write("\n!aGmref = nulref")

    for aChildItem in theTreeItem.Member:
        exportSdte(aChildItem, thePmlFile)
        exportText(aChildItem, thePmlFile)
        exportPtse(aChildItem, thePmlFile)
        exportGmse(aChildItem, thePmlFile)
        exportScom(aChildItem, thePmlFile)
    # for
# exportCate

def exportSdte(theTreeItem, thePmlFile):
    if theTreeItem.Type != "SDTE":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SDTEXT /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SDTEXT")
    # if

    thePmlFile.write("\nSKEY '%s'" % theTreeItem.Skey)
    thePmlFile.write("\nRTEX (|%s|)" % theTreeItem.Rtext)
    thePmlFile.write("\nSTEX |%s|" % theTreeItem.Stext)
# exportSdte

def exportText(theTreeItem, thePmlFile):
    if theTreeItem.Type != "TEXT":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW TEXT /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW TEXT")
    # if

    thePmlFile.write("\nSTEX |%s|" % theTreeItem.Stext)
# exportText

def exportScom(theTreeItem, thePmlFile):
    if theTreeItem.Type != "SCOM":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SCOMPONENT /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SCOMPONENT")
    # if

    thePmlFile.write("\n!!ce.Ptref = !aPtref")
    thePmlFile.write("\n!!ce.Gmref = !aGmref")

    thePmlFile.write("\nGTYP %s" % theTreeItem.Gtype)
    thePmlFile.write("\nPARA %s" % theTreeItem.Param)

# exportScom

def exportPtse(theTreeItem, thePmlFile):
    if theTreeItem.Type != "PTSE":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW PTSET /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW PTSET")
    # if

    thePmlFile.write("\n!aCategory.Ptref = ce")
    thePmlFile.write("\n!aPtref = ce")

    for aPntItem in theTreeItem.Member:
        exportPtax(aPntItem, thePmlFile)
        exportPtca(aPntItem, thePmlFile)
    # for

# exportPtse

def exportPtax(theTreeItem, thePmlFile):
    if theTreeItem.Type != "PTCA":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW PTCAR /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW PTCAR")
    # if

    aPx = theTreeItem.Px.replace("math.tan", "TAN")
    aPx = aPx.replace("math.pi", "180")

    aPy = theTreeItem.Py.replace("math.tan", "TAN")
    aPy = aPy.replace("math.pi", "180")

    aPz = theTreeItem.Pz.replace("math.tan", "TAN")
    aPz = aPz.replace("math.pi", "180")

    thePmlFile.write("\nNUMB %d" % theTreeItem.Number)

    if len(theTreeItem.Connection) > 0:
        thePmlFile.write("\nPCON %s" % theTreeItem.Connection)
    # if

    if len(theTreeItem.Bore) > 0:
        thePmlFile.write("\nPBOR %s" % theTreeItem.Bore)
    # if

    if len(theTreeItem.Direction) > 0:
        thePmlFile.write("\nPtcdirection %s" % theTreeItem.Direction)
    # if

    if len(aPx) > 0:
        if aPx.startswith("DD"):
            thePmlFile.write("\nPX %s" % aPx)
        else:
            thePmlFile.write("\nPX (%s)" % aPx)
        # if
    # if

    if len(aPy) > 0:
        if aPy.startswith("DD"):
            thePmlFile.write("\nPY %s" % aPy)
        else:
            thePmlFile.write("\nPY (%s)" % aPy)
        # if
    # if

    if len(aPz) > 0:
        if aPz.startswith("DD"):
            thePmlFile.write("\nPZ %s" % aPz)
        else:
            thePmlFile.write("\nPZ (%s)" % aPz)
        # if
    # if

# exportPtax

def exportPtca(theTreeItem, thePmlFile):
    if theTreeItem.Type != "PTAX":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW PTAXIS /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW PTAXIS")
    # if

    aPdis = theTreeItem.Distance.replace("math.tan", "TAN")
    aPdis = aPdis.replace("math.pi", "180")

    thePmlFile.write("\nNUMB %d" % theTreeItem.Number)

    if len(theTreeItem.Connection) > 0:
        thePmlFile.write("\nPCON %s" % theTreeItem.Connection)
    # if

    if len(theTreeItem.Bore) > 0:
        thePmlFile.write("\nPBOR %s" % theTreeItem.Bore)
    # if

    if len(aPdis) > 0:
        if aPdis.startswith("DD"):
            thePmlFile.write("\nPDIS %s" % aPdis)
        else:
            thePmlFile.write("\nPDIS (%s)" % aPdis)
        # if
    # if

    if len(theTreeItem.Axis) > 0:
        thePmlFile.write("\nPAXI %s" % theTreeItem.Axis)
    # if
# exportPtca

def exportGmse(theTreeItem, thePmlFile):
    if theTreeItem.Type != "GMSE":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW GMSET /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW GMSET")
    # if

    thePmlFile.write("\n!aCategory.Gmref = ce")
    thePmlFile.write("\n!aGmref = ce")

    for aChildItem in theTreeItem.Member:
        exportSbox(aChildItem, thePmlFile)
        exportScyl(aChildItem, thePmlFile)
        exportLsno(aChildItem, thePmlFile)
        exportSdsh(aChildItem, thePmlFile)
        exportScto(aChildItem, thePmlFile)
    # for

# exportGmse

def exportSbox(theTreeItem, thePmlFile):
    if theTreeItem.Type != "SBOX":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SBOX /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SBOX")
    # if

    thePmlFile.write("\nTuflag True")

    if len(theTreeItem.Px) > 0:
        thePmlFile.write("\nPx (%s)" % theTreeItem.Px)
    # if

    if len(theTreeItem.Py) > 0:
        thePmlFile.write("\nPy (%s)" % theTreeItem.Py)
    # if

    if len(theTreeItem.Pz) > 0:
        thePmlFile.write("\nPz (%s)" % theTreeItem.Pz)
    # if

    if len(theTreeItem.Pxlength) > 0:
        thePmlFile.write("\nPxlength (%s)" % theTreeItem.Pxlength)
    # if

    if len(theTreeItem.Pylength) > 0:
        thePmlFile.write("\nPylength (%s)" % theTreeItem.Pylength)
    # if

    if len(theTreeItem.Pzlength) > 0:
        thePmlFile.write("\nPzlength (%s)" % theTreeItem.Pzlength)
    # if

# exportSbox

def exportScyl(theTreeItem, thePmlFile):
    if theTreeItem.Type != "SCYL":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SCYLINDER /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SCYLINDER")
    # if

    thePmlFile.write("\nTuflag True")

    if len(theTreeItem.Distance) > 0:
        thePmlFile.write("\nPdistance (%s)" % theTreeItem.Distance)
    # if

    if len(theTreeItem.Diameter) > 0:
        thePmlFile.write("\nPdiameter (%s)" % theTreeItem.Diameter)
    # if

    if len(theTreeItem.Height) > 0:
        thePmlFile.write("\nPheight (%s)" % theTreeItem.Height)
    # if

    if len(theTreeItem.Axis) > 0:
        thePmlFile.write("\nPaxis %s" % theTreeItem.Axis)
    # if

# exportScyl

def exportLsno(theTreeItem, thePmlFile):
    if theTreeItem.Type != "LSNO":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW LSNOUT /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW LSNOUT")
    # if

    thePmlFile.write("\nTuflag True")

    exportParam(thePmlFile, "Ptdistance", theTreeItem.Tdistance)
    exportParam(thePmlFile, "Pbdistance", theTreeItem.Bdistance)
    exportParam(thePmlFile, "Ptdiameter", theTreeItem.Tdiameter)
    exportParam(thePmlFile, "Pbdiameter", theTreeItem.Bdiameter)
    exportParam(thePmlFile, "Poffset", theTreeItem.Offset)

    if len(theTreeItem.Aaxis) > 0:
        thePmlFile.write("\nPaaxis %s" % theTreeItem.Aaxis)
    # if

    if len(theTreeItem.Baxis) > 0:
        thePmlFile.write("\nPbaxis %s" % theTreeItem.Baxis)
    # if

# exportLsno

def exportSdsh(theTreeItem, thePmlFile):
    if theTreeItem.Type != "SDSH":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SDSH /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SDSH")
    # if

    thePmlFile.write("\nTuflag True")

    if len(theTreeItem.Axis) > 0:
        thePmlFile.write("\nPaxis %s" % theTreeItem.Axis)
    # if

    exportParam(thePmlFile, "Pdistance", theTreeItem.Distance)
    exportParam(thePmlFile, "Pheight", theTreeItem.Height)
    exportParam(thePmlFile, "Pradius", theTreeItem.Radius)
    exportParam(thePmlFile, "Pdiameter", theTreeItem.Diameter)

# exportSdsh

def exportScto(theTreeItem, thePmlFile):
    if theTreeItem.Type != "SCTO":
        return
    # if

    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW SCTORUS /%s" % theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW SCTORUS")
    # if

    thePmlFile.write("\nTuflag True")

    if len(theTreeItem.Aaxis) > 0:
        thePmlFile.write("\nPaaxis %s" % theTreeItem.Aaxis)
    # if

    if len(theTreeItem.Baxis) > 0:
        thePmlFile.write("\nPbaxis %s" % theTreeItem.Baxis)
    # if

    exportParam(thePmlFile, "Pdiameter", theTreeItem.Diameter)

# exportScto

def exportEquipment(theTreeItem, thePmlFile):
    if theTreeItem.Type != "EQUI":
        return
    # if

    aPos = theTreeItem.Position
    if len(theTreeItem.Name) > 0:
        thePmlFile.write("\nNEW EQUIPMENT /" + theTreeItem.Name)
    else:
        thePmlFile.write("\nNEW EQUIPMENT")
    # if
    thePmlFile.write("\nPOS E%f N%f U%f" % (aPos.X, aPos.Y, aPos.Z))
    thePmlFile.write("\n")

    for aItem in theTreeItem.Member:
        if aItem.Type == "CYLI":
            # Cylinder
            thePmlFile.write("\nNEW CYLINDER DIAM %f HEIG %f" % (aItem.Diameter, aItem.Height) )
        elif aItem.Type == "BOX":
            # Box
            thePmlFile.write("\nNEW BOX XLEN %f YLEN %f ZLEN %f" % (aItem.Xlength, aItem.Ylength, aItem.Zlength))
        elif aItem.Type == "DISH":
            # Dish
            thePmlFile.write("\nNEW DISH DIAM %f HEIG %f RADI %f" % (aItem.Diameter, aItem.Height, aItem.Radius))
        elif aItem.Type == "CONE":
            # Cone
            thePmlFile.write("\nNEW CONE DTOP %f DBOT %f HEIG %f" % (aItem.Tdiameter, aItem.Bdiameter, aItem.Height))
        elif aItem.Type == "EXTR":
            # Extrusion
            thePmlFile.write("\nNEW EXTR HEIG %f" % (aItem.Height))
            thePmlFile.write("\n!aExtrItem = ce")
            for aChildItem in aItem.Member:
                if aChildItem.Type == "LOOP":
                    thePmlFile.write("\nNEW LOOP")
                    for aVertItem in aChildItem.Member:
                        aPnt = aVertItem.Position
                        thePmlFile.write("\nNEW VERT POS E%f N%f U%f" % (aPnt.X, aPnt.Y, aPnt.Z))
                    # for
                elif aChildItem.Type == "NXTR":
                    thePmlFile.write("\nNEW NXTR HEIG %f" % (aChildItem.Height))
                    for aLoopItem in aChildItem.Member:
                        thePmlFile.write("\nNEW LOOP")
                        for aVertItem in aLoopItem.Member:
                            aPnt = aVertItem.Position
                            thePmlFile.write("\nNEW VERT POS E%f N%f U%f" % (aPnt.X, aPnt.Y, aPnt.Z))
                        # for
                    # for
                # if
            # for
            thePmlFile.write("\n!!ce = !aExtrItem")
        elif aItem.Type == "NOZZ":
            # Nozzle
            if len(aItem.Name) > 0:
                thePmlFile.write("\nNEW NOZZ /%s HEIG %f" % (aItem.Name, aItem.Height))
            else:
                thePmlFile.write("\nNEW NOZZ HEIG %f" % (aItem.Height))
            # if

            aCatref = aItem.Catref
            if aCatref is not None:
                thePmlFile.write("\nCATR SCOMPONENT /" + aCatref.Name)
                thePmlFile.write("\nhandle ANY")
                thePmlFile.write("\n $p Bad Catref of Nozzle " + aItem.Name)
                thePmlFile.write("\nendhandle")
            # if
        else:
            continue
        # if

        # Output position and orientation.
        aPos = aItem.Position
        aOri = aItem.Orientation
        aDy = aOri.YDirection
        aDz = aOri.ZDirection
        thePmlFile.write("\nPOS E%f N%f U%f" % (aPos.X, aPos.Y, aPos.Z))
        thePmlFile.write("\n!aDy = object Direction('N')")
        thePmlFile.write("\n!aDz = object Direction('U')")
        thePmlFile.write("\n!aDy.east = %f" % aDy.x)
        thePmlFile.write("\n!aDy.north = %f" % aDy.y)
        thePmlFile.write("\n!aDy.up = %f" % aDy.z)
        thePmlFile.write("\n!aDz.east = %f" % aDz.x)
        thePmlFile.write("\n!aDz.north = %f" % aDz.y)
        thePmlFile.write("\n!aDz.up = %f" % aDz.z)
        thePmlFile.write("\nORI Y is $!aDy and Z is $!aDz")
        thePmlFile.write("\n")
    # for
# exportEquipment

def Export():
    aTreeItem = PipeCad.CurrentItem()
    if aTreeItem is None:
        QMessageBox.critical(PipeCad, "", PipeCad.tr("Please select item to export!"))
        return
    # if

    aFileName = QFileDialog.getSaveFileName(PipeCad, PipeCad.tr("Export PDMS PML"), "", PipeCad.tr("PDMS PML Macro (*.pml)"))
    if len(aFileName) < 1:
        return
    # if

    aPmlFile = open(aFileName, "w")

    # PML Macro Header.
    aPmlFile.write("$S-  -- Synonym translation OFF")
    aPmlFile.write("\n-- ----------------------------------------------------------------")
    aPmlFile.write("\n-- Data Listing    Date : " + time.asctime(time.localtime(time.time())))
    aPmlFile.write("\n-- Exported by PipeCAD.\n")

    aPmlFile.write("\nONERROR GOLABEL /ERROR3\n")
    aPmlFile.write("\nINPUT BEGIN")

    # PML Macro Content.
    exportEquipment(aTreeItem, aPmlFile)

    exportCatalogue(aTreeItem, aPmlFile)

    aPmlFile.write("\nINPUT END %s" % aTreeItem.Type)
    aPmlFile.write("\nINPUT FINISH\n")

    # Handle Exception.
    aPmlFile.write("\n-- Switch synonyms back on if an error occurs.")
    aPmlFile.write("\nLABEL /ERROR3")
    aPmlFile.write("\nhandle ANY")
    aPmlFile.write("\n$S+")
    aPmlFile.write("\nRETURN ERROR")
    aPmlFile.write("\nendhandle\n")

    # PML Macro Footer.
    aPmlFile.write("\n-- End Data Listing    Date : " + time.asctime(time.localtime(time.time())))
    aPmlFile.write("\n$S+  -- Synonym translation ON")
    aPmlFile.write("\n-- ----------------------------------------------------------------")
    aPmlFile.write("\n")

    aPmlFile.close()

    QMessageBox.information(PipeCad, "", "Export PDMS PML Finished!")
# Export
