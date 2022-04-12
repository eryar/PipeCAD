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
from PythonQt.PipeCAD import *

from PipeCAD import *

import time


def Export():
    aTreeItem = PipeCad.CurrentItem()
    if aTreeItem is None:
        QMessageBox.critical(PipeCad, "", PipeCad.tr("Please select item to export!"))
        return
    # if

    if aTreeItem.Type != "EQUI":
        QMessageBox.critical(PipeCad, "", PipeCad.tr("Please select equipment item to export!"))
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

    # PML Macro Content.
    aPos = aTreeItem.Position
    aPmlFile.write("\nINPUT BEGIN")
    if len(aTreeItem.Name) > 0:
        aPmlFile.write("\nNEW EQUIPMENT /" + aTreeItem.Name)
    else:
        aPmlFile.write("\nNEW EQUIPMENT")
    # if
    aPmlFile.write("\nPOS E%f N%f U%f" % (aPos.x, aPos.y, aPos.z))
    aPmlFile.write("\n")

    for aItem in aTreeItem.Member:
        if aItem.Type == "CYLI":
            # Cylinder
            aPmlFile.write("\nNEW CYLINDER DIAM %f HEIG %f" % (aItem.Diameter, aItem.Height) )
        elif aItem.Type == "BOX":
            # Box
            aPmlFile.write("\nNEW BOX XLEN %f YLEN %f ZLEN %f" % (aItem.Xlength, aItem.Ylength, aItem.Zlength))
        elif aItem.Type == "DISH":
            # Dish
            aPmlFile.write("\nNEW DISH DIAM %f HEIG %f RADI %f" % (aItem.Diameter, aItem.Height, aItem.Radius))
        elif aItem.Type == "CONE":
            # Cone
            aPmlFile.write("\nNEW CONE DTOP %f DBOT %f HEIG %f" % (aItem.Tdiameter, aItem.Bdiameter, aItem.Height))
        elif aItem.Type == "EXTR":
            # Extrusion
            aPmlFile.write("\nNEW EXTR HEIG %f" % (aItem.Height))
            aPmlFile.write("\n!aExtrItem = ce")
            for aChildItem in aItem.Member:
                if aChildItem.Type == "LOOP":
                    aPmlFile.write("\nNEW LOOP")
                    for aVertItem in aChildItem.Member:
                        aPnt = aVertItem.Position
                        aPmlFile.write("\nNEW VERT POS E%f N%f U%f" % (aPnt.x, aPnt.y, aPnt.z))
                    # for
                elif aChildItem.Type == "NXTR":
                    aPmlFile.write("\nNEW NXTR HEIG %f" % (aChildItem.Height))
                    for aLoopItem in aChildItem.Member:
                        aPmlFile.write("\nNEW LOOP")
                        for aVertItem in aLoopItem.Member:
                            aPnt = aVertItem.Position
                            aPmlFile.write("\nNEW VERT POS E%f N%f U%f" % (aPnt.x, aPnt.y, aPnt.z))
                        # for
                    # for
                # if
            # for
            aPmlFile.write("\n!!ce = !aExtrItem")
        elif aItem.Type == "NOZZ":
            # Nozzle
            if len(aItem.Name) > 0:
                aPmlFile.write("\nNEW NOZZ /%s HEIG %f" % (aItem.Name, aItem.Height))
            else:
                aPmlFile.write("\nNEW NOZZ HEIG %f" % (aItem.Height))
            # if

            aCatref = aItem.Catref
            if aCatref is not None:
                aPmlFile.write("\nCATR SCOMPONENT /" + aCatref.Name)
                aPmlFile.write("\nhandle ANY")
                aPmlFile.write("\n $p Bad Catref of Nozzle " + aItem.Name)
                aPmlFile.write("\nendhandle")
            # if
        else:
            continue
        # if

        # Output position and orientation.
        aPos = aItem.Position
        aOri = aItem.Orientation
        aDy = aOri.YDirection
        aDz = aOri.ZDirection
        aPmlFile.write("\nPOS E%f N%f U%f" % (aPos.x, aPos.y, aPos.z))
        aPmlFile.write("\n!aDy = object Direction('N')")
        aPmlFile.write("\n!aDz = object Direction('U')")
        aPmlFile.write("\n!aDy.east = %f" % aDy.x)
        aPmlFile.write("\n!aDy.north = %f" % aDy.y)
        aPmlFile.write("\n!aDy.up = %f" % aDy.z)
        aPmlFile.write("\n!aDz.east = %f" % aDz.x)
        aPmlFile.write("\n!aDz.north = %f" % aDz.y)
        aPmlFile.write("\n!aDz.up = %f" % aDz.z)
        aPmlFile.write("\nORI Y is $!aDy and Z is $!aDz")
        aPmlFile.write("\n")
    # for

    aPmlFile.write("\nINPUT END EQUIPMENT")
    aPmlFile.write("\nINPUT FINISH")

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
