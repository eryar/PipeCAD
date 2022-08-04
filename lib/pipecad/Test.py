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
# Date: 21:16 2021-09-16

from PythonQt.QtCore import *
from PythonQt.QtGui import *
from PythonQt.QtSql import *
from PythonQt.pipecad import *

from pipecad import *


def E1301():
    PipeCad.StartTransaction("Equipment E1301")
    PipeCad.CreateItem("EQUI", "E1301")

    aEquiItem = PipeCad.CurrentItem()
    aEquiItem.Position= Position("2850 5660 1470", aEquiItem.Owner)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 460
    aShapeItem.Ylength = 300
    aShapeItem.Zlength = 630
    aShapeItem.Position= Position("0 1710 -315", aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 460
    aShapeItem.Ylength = 300
    aShapeItem.Zlength = 630
    aShapeItem.Position= Position("0 5370 -315", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 960
    aShapeItem.Height = 120
    aShapeItem.Position= Position("0 60 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 860
    aShapeItem.Height = 428
    aShapeItem.Position= Position("0 334 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 960
    aShapeItem.Height = 240
    aShapeItem.Position= Position("0 668 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 860
    aShapeItem.Height = 5690
    aShapeItem.Position= Position("0 3633 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 1020
    aShapeItem.Height = 240
    aShapeItem.Position= Position("0 6598 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 910
    aShapeItem.Height = 180
    aShapeItem.Position= Position("0 6808 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("DISH")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 910
    aShapeItem.Height = 200
    aShapeItem.Position= Position("0 6898 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "E1301-S1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 250
    aNozzItem.Position= Position("0 3540 -635", aEquiItem)
    aNozzItem.Orientation = Orientation(0, -90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "E1301-S2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 250
    aNozzItem.Position= Position("0 1100 635", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "E1301-S3")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 250
    aNozzItem.Position= Position("0 5980 635", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    # PipeCad.CreateItem("NOZZ", "E1301-T1")
    # aNozzItem = PipeCad.CurrentItem()
    # aNozzItem.Catref = "/AAZFBB0NN"
    # aNozzItem.Height = 250
    # aNozzItem.Position= "0 290 635"
    # aNozzItem.Orientation = "1 0 0 0 0 -1"

    # PipeCad.CreateItem("NOZZ", "E1301-T2")
    # aNozzItem = PipeCad.CurrentItem()
    # aNozzItem.Catref = "/AAZFBB0NN"
    # aNozzItem.Height = 250
    # aNozzItem.Position= "0 290 -635"
    # aNozzItem.Orientation = "-1 0 0 0 0 1"

    PipeCad.CommitTransaction()
# E1301

def C1101():
    PipeCad.StartTransaction("Equipment C1101")
    PipeCad.CreateItem("EQUI", "C1101")

    aEquiItem = PipeCad.CurrentItem()
    aEquiItem.Position= Position("5360 8850 305", aEquiItem.Owner)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 2000
    aShapeItem.Height = 46
    aShapeItem.Position= Position("0 0 23", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 1913
    aShapeItem.Height = 14000
    aShapeItem.Position= Position("0 0 7046", aEquiItem)

    PipeCad.CreateItem("CONE")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Tdiameter = 1567
    aShapeItem.Bdiameter = 1913
    aShapeItem.Height = 280
    aShapeItem.Position= Position("0 0 14186", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 1567
    aShapeItem.Height = 7849
    aShapeItem.Position= Position("0 0 18250.5", aEquiItem)

    PipeCad.CreateItem("DISH")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 1567
    aShapeItem.Height = 300
    aShapeItem.Radius = 70
    aShapeItem.Position= Position("0 0 22175", aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0NN")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("0 1088 940", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, -90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0VV")
    aNozzItem.Height = 300
    aNozzItem.Position= Position("-1088 380 3581", aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N3")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("-1088 0 4521", aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N4")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 200
    aNozzItem.Position= Position("-381 1037 13350", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, -90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N5")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 320
    aNozzItem.Position= Position("0 1088 21539", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, -90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N6")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0TT")
    aNozzItem.Height = 300
    aNozzItem.Position= Position("0 0 22657", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N7")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("942.24 544 1676", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, -150, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N8")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("942.24 544 4114", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, -150, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N9")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("942.24 -544 1676", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 150, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N10")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("942.24 -544 4419", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 150, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N11")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0HH")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("459.81 -986.06 9754", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 115, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-N12")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("126.79 271.89 22581", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-M1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0ZZ")
    aNozzItem.Height = 250
    aNozzItem.Position= Position("0 -1150 2286", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-M2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0ZZ")
    aNozzItem.Height = 250
    aNozzItem.Position= Position("0 -1150 13411", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "C1101-M3")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0ZZ")
    aNozzItem.Height = 450
    aNozzItem.Position= Position("0 -1150 21564", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 90, aEquiItem)

    PipeCad.CommitTransaction()
# C1101

def P1501A():
    PipeCad.StartTransaction("Equipment P1501A")
    PipeCad.CreateItem("EQUI", "P1501A")

    aEquiItem = PipeCad.CurrentItem()
    aEquiItem.Position= Position("9340 12145 645", aEquiItem.Owner)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 370
    aShapeItem.Height = 400
    aShapeItem.Position= Position("0 1074 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 510
    aShapeItem.Ylength = 200
    aShapeItem.Zlength = 230
    aShapeItem.Position= Position("0 174 -115", aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 510
    aShapeItem.Ylength = 1390
    aShapeItem.Zlength = 110
    aShapeItem.Position= Position("0 654 -285", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 200
    aShapeItem.Height = 500
    aShapeItem.Position= Position("0 324 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("0 624 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 200
    aShapeItem.Height = 100
    aShapeItem.Position= Position("0 724 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("0 824 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 250
    aShapeItem.Ylength = 300
    aShapeItem.Zlength = 100
    aShapeItem.Position= Position("0 1074 -180", aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1501A-N1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0NN")
    aNozzItem.Height = 155
    aNozzItem.Position= Position("0 0 0", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1501A-N2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 180
    aNozzItem.Position= Position("-135 155 180", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CommitTransaction()
# P1501A

def P1501B():
    PipeCad.StartTransaction("Equipment P1501B")
    PipeCad.CreateItem("EQUI", "P1501B")

    aEquiItem = PipeCad.CurrentItem()
    aEquiItem.Position= Position("7510 12145 645", aEquiItem.Owner)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 370
    aShapeItem.Height = 400
    aShapeItem.Position= Position("0 1074 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 510
    aShapeItem.Ylength = 200
    aShapeItem.Zlength = 230
    aShapeItem.Position= Position("0 174 -115", aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 510
    aShapeItem.Ylength = 1390
    aShapeItem.Zlength = 110
    aShapeItem.Position= Position("0 654 -285", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 200
    aShapeItem.Height = 500
    aShapeItem.Position= Position("0 324 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("0 624 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 200
    aShapeItem.Height = 100
    aShapeItem.Position= Position("0 724 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("0 824 0", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 250
    aShapeItem.Ylength = 300
    aShapeItem.Zlength = 100
    aShapeItem.Position= Position("0 1074 -180", aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1501B-N1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0NN")
    aNozzItem.Height = 155
    aNozzItem.Position= Position("0 0 0", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 90, aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1501B-N2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 180
    aNozzItem.Position= Position("-135 155 180", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CommitTransaction()
# P1501B

def P1502A():
    PipeCad.StartTransaction("Equipment P1502A")
    PipeCad.CreateItem("EQUI", "P1502A")

    aEquiItem = PipeCad.CurrentItem()
    aEquiItem.Position= Position("12490 12280 1150", aEquiItem.Owner)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 600
    aShapeItem.Height = 700
    aShapeItem.Position= Position("190 1350.5 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 790
    aShapeItem.Ylength = 1680
    aShapeItem.Zlength = 130
    aShapeItem.Position= Position("190 715 -780", aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 440
    aShapeItem.Ylength = 203
    aShapeItem.Zlength = 410
    aShapeItem.Position= Position("190 75 -510", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 440
    aShapeItem.Height = 400
    aShapeItem.Position= Position("190 75 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CONE")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Tdiameter = 250
    aShapeItem.Bdiameter = 440
    aShapeItem.Height = 325
    aShapeItem.Position= Position("190 437.5 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("190 650 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 200
    aShapeItem.Height = 200
    aShapeItem.Position= Position("190 800 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("190 950 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 500
    aShapeItem.Ylength = 200
    aShapeItem.Zlength = 410
    aShapeItem.Position= Position("190 1270 -510", aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1502A-N1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0NN")
    aNozzItem.Height = 100
    aNozzItem.Position= Position("255 75 0", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1502A-N2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 305
    aNozzItem.Position= Position("0 0 0", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CommitTransaction()
# P1502A

def P1502B():
    PipeCad.StartTransaction("Equipment P1502B")
    PipeCad.CreateItem("EQUI", "P1502B")

    aEquiItem = PipeCad.CurrentItem()
    aEquiItem.Position= Position("14880 12280 1150", aEquiItem.Owner)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 360
    aShapeItem.Height = 700
    aShapeItem.Position= Position("190 1350.5 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 790
    aShapeItem.Ylength = 1680
    aShapeItem.Zlength = 130
    aShapeItem.Position= Position("190 715 -780", aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 440
    aShapeItem.Ylength = 203
    aShapeItem.Zlength = 410
    aShapeItem.Position= Position("190 75 -510", aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 440
    aShapeItem.Height = 400
    aShapeItem.Position= Position("190 75 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CONE")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Tdiameter = 250
    aShapeItem.Bdiameter = 440
    aShapeItem.Height = 325
    aShapeItem.Position= Position("190 437.5 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("190 650 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 200
    aShapeItem.Height = 200
    aShapeItem.Position= Position("190 800 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("CYLI")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Diameter = 100
    aShapeItem.Height = 100
    aShapeItem.Position= Position("190 950 -305", aEquiItem)
    aShapeItem.Orientation = Orientation(-90, 0, 0, aEquiItem)

    PipeCad.CreateItem("BOX")
    aShapeItem = PipeCad.CurrentItem()
    aShapeItem.Xlength = 500
    aShapeItem.Ylength = 200
    aShapeItem.Zlength = 410
    aShapeItem.Position= Position("190 1270 -510", aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1502B-N1")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0NN")
    aNozzItem.Height = 150
    aNozzItem.Position= Position("255 75 0", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1502B-N2")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0JJ")
    aNozzItem.Height = 305
    aNozzItem.Position= Position("0 0 0", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 90, 0, aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1502B-N3")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0LL")
    aNozzItem.Height = 310
    aNozzItem.Position= Position("500 1550 -245", aEquiItem)
    aNozzItem.Orientation = Orientation(0, 0, 180, aEquiItem)

    PipeCad.CreateItem("NOZZ", "P1502B-N4")
    aNozzItem = PipeCad.CurrentItem()
    aNozzItem.Catref = PipeCad.GetItem("/AAZFBD0RR")
    aNozzItem.Height = 305
    aNozzItem.Position= Position("-115 1220 -435", aEquiItem)

    PipeCad.CommitTransaction()
# P1502B
