from PythonQt.QtCore import *
from PythonQt.QtGui import *

from pipecad import *

import omp 
import json
import os
import math 
import pandas as pd

class ArrivePoint( QGraphicsEllipseItem ) :
    def __init__( self, parent = None ):
        super( ArrivePoint, self ).__init__( QRectF( -5.0, -5.0, 10.0, 10.0) )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        pen_arrive = QPen( QColor( 51, 51, 255 ) )
        pen_arrive.setWidth( 2 )
        pen_arrive.setStyle( Qt.SolidLine )   
        self.setPen( pen_arrive )

class LeavePoint( QGraphicsEllipseItem ) :
    def __init__( self, parent = None ):
        super( LeavePoint, self ).__init__( QRectF( -5.0, -5.0, 10.0, 10.0) )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        pen_leave = QPen( QColor( 255, 0, 0 ) )
        pen_leave.setWidth( 2 )
        pen_leave.setStyle( Qt.SolidLine )   
        self.setPen( pen_leave )
        
class TeePoint( QGraphicsEllipseItem ) :
    def __init__( self, parent = None ):
        super( TeePoint, self ).__init__( QRectF( -5.0, -5.0, 10.0, 10.0) )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        pen_tee = QPen( Qt.magenta )
        pen_tee.setWidth( 2 )
        pen_tee.setStyle( Qt.SolidLine )   
        self.setPen( pen_tee )

class SpindlePoint( QGraphicsEllipseItem ) :
    def __init__( self, parent = None ):
        super( SpindlePoint, self ).__init__( QRectF( -5.0, -5.0, 10.0, 10.0) )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        pen_spindle = QPen( QColor( 111, 0, 0 ) )
        pen_spindle.setWidth( 2 )
        pen_spindle.setStyle( Qt.SolidLine )   
        self.setPen( pen_spindle )
                 
      
class SheetLayout( QGraphicsScene ):
    def __init__( self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor_coordinates = []
        
        self.symbol_drawlist_temp = []
        self.symbol_drawlist = []
        self.grid_drawlist = []
        
        self.arrive_point = ArrivePoint( self )
        self.leave_point = LeavePoint( self )
        self.tee_point = TeePoint( self )
        self.spindle_point = SpindlePoint( self )
        self.line = QGraphicsLineItem()
        self.rect = QGraphicsRectItem()
        self.triangle = QGraphicsPolygonItem()
        
        self.sheet_width = 400
        self.sheet_height = 400
        self.step_x = 5
        self.step_y = 5
        self.origin_x = 0
        self.origin_y = 0
       
        #self.scale = 1.0
        
        self.show_grids = False 
        self.current_action = ""
        self.press_number = 0
        self.cursor_position = QPoint( 0, 0 )
        self.point_diameter = 5
                
        self.draw_grid()
    
    def draw_grid_labels( self ):
        print( "test" )

    def convert_to_relative_position( self, scene_position ):
        new_position = QPointF( round ( ( scene_position.x() - self.sheet_width / 2 ) / self.step_x / 20 , 3 ), 
                                round ( ( self.sheet_height / 2 - scene_position.y() ) / self.step_y / 20 , 3 ) ) 
                   
                    
        return new_position        
    
    def convert_to_absolute_position( self, relative_position ):
        new_position = QPointF( round ( ( relative_position.x() - self.sheet_width / 2 ) / self.step_x / 20 , 2 ), 
                                round ( ( self.sheet_height / 2 - relative_position.y() ) / self.step_y / 20 , 2 ) )               
        return new_position        
    
    def draw_grid( self ):
        
        width = self.sheet_width
        height = self.sheet_height
        
        self.setSceneRect( 0, 0, width, height )
        self.setItemIndexMethod( QGraphicsScene.NoIndex )
        
        pen_axis = QPen( QColor( 126, 128, 135 ) )
        pen_axis.setWidth( 1 )
        pen_axis.setStyle( Qt.SolidLine )    
                
        pen_grid_main = QPen( QColor( 212, 212, 212 ) )
        pen_grid_main.setWidth( 1 )
        pen_grid_main.setStyle( Qt.SolidLine )    
        
        pen_grid_sec = QPen( QColor( 250, 250, 250 ) )
        pen_grid_sec.setWidth( 0.5 )
        pen_grid_sec.setStyle( Qt.SolidLine )  
        
        for x in range( 0, int( self.sheet_width / self.step_x ) + 1 ):
            xc = x * self.step_x
            if x % 10 == 0:
                label_text = str( ( xc - self.sheet_width / 2 ) / 100 ) 
                label = QGraphicsSimpleTextItem( label_text )
                label_width = label.boundingRect().size().width()
                label_height = label.boundingRect().size().height()
                label_pos_x = xc - label_width / 2
                label_pos_y = self.sheet_height + label_height / 2
                label.setPos( label_pos_x, label_pos_y )
                self.addItem( label )   
        
            if x % 10 == 0:
                if x == int( self.sheet_width / self.step_x / 2 ):
                    self.grid_drawlist.append( self.addLine( xc, 0, xc, height, pen_axis ) )
                else:
                    self.grid_drawlist.append( self.addLine( xc, 0, xc, height, pen_grid_main ) )
            else: 
                self.grid_drawlist.append( self.addLine( xc, 0, xc, height, pen_grid_sec ) )

        for y in range( 0, int( self.sheet_height / self.step_y ) + 1 ):
            yc = y * self.step_y

            if y % 10 == 0 and int( ( self.sheet_height / 2 - yc ) / 10 ) != -20:
                label_text = str(  ( self.sheet_height / 2 - yc ) / 100  ) 
                label = QGraphicsSimpleTextItem( label_text )
                label_width = label.boundingRect().size().width()
                label_height = label.boundingRect().size().height()
                label_pos_x = - label_width - 5
                label_pos_y = yc - label_height / 2
                label.setPos( label_pos_x, label_pos_y )
                self.addItem( label )  
                
            if y % 10 == 0:
                if y == int( self.sheet_height / self.step_x / 2 ):
                    self.grid_drawlist.append( self.addLine( 0, yc, width, yc, pen_axis ) )
                else:
                    self.grid_drawlist.append( self.addLine( 0, yc, width, yc, pen_grid_main ) )
            else: 
                self.grid_drawlist.append( self.addLine( 0, yc, width, yc, pen_grid_sec ) )
            
    def set_grid_center( self, grid_center = "Center" ):
        if grid_center == "Center":
            self.origin_x = self.sheet_width / 2 
            self.origin_y = self.sheet_height / 2 
        
    def set_visible( self, visible = True ):
        for line in self.grid_drawlist:
            line.setVisible(visible)

    def delete_grid( self ):
        for line in self.grid_drawlist:
            self.removeItem(line)
        del self.grid_drawlist[:]

    def set_opacity( self, opacity ):
        for line in self.grid_drawlist:
            line.setOpacity( opacity )
    
    def keyPressEvent( self, event ):
        if event.key() == ( Qt.Key_Control and Qt.Key_Z ):
            self.undo()
        elif event.key() == ( Qt.Key_Control and Qt.Key_Y ):
            self.redo()
        elif event.key() == ( Qt.Key_Escape ):
            self.press_number = 0
            self.current_action = ""
            QApplication.restoreOverrideCursor()
            for item in self.symbol_drawlist_temp:
                self.removeItem( item )

    def undo( self ):
        print( "Delete the last line from self.drawlist and draw all the others" )
        
    def redo( self ):
        print( "Delete the last line from self.drawlist and draw all the others" )
      
    def mousePressEvent( self, mouse_event ):
        self.cursor_position = QPointF( mouse_event.scenePos().x(), mouse_event.scenePos().y() )
        if mouse_event.button() == Qt.LeftButton and self.current_action == "draw_arrive_point":
                self.cursor_coordinates.append( self.cursor_position )
                self.draw_arrive_point( self.cursor_coordinates )             
                self.press_number = 0
                self.current_action = ""
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )
                    
        elif mouse_event.button() == Qt.LeftButton and self.current_action == "draw_leave_point":
                self.cursor_coordinates.append( self.cursor_position )
                self.draw_leave_point( self.cursor_coordinates )             
                self.press_number = 0
                self.current_action = ""
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )
                          
        elif mouse_event.button() == Qt.LeftButton and self.current_action == "draw_tee_point":
                self.cursor_coordinates.append( self.cursor_position )
                self.draw_tee_point( self.cursor_coordinates )             
                self.press_number = 0
                self.current_action = ""
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )
                    
        elif mouse_event.button() == Qt.LeftButton and self.current_action == "draw_spindle_point":
                self.cursor_coordinates.append( self.cursor_position )
                self.draw_spindle_point( self.cursor_coordinates )             
                self.press_number = 0
                self.current_action = ""
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )
                    
        elif mouse_event.button() == Qt.LeftButton and self.current_action == "draw_line":
            self.press_number = self.press_number + 1
            if self.press_number == 1:
                self.cursor_coordinates.append( self.cursor_position )
            elif self.press_number == 2: 
                self.cursor_coordinates.append( self.cursor_position ) 
                self.draw_line( self.cursor_coordinates )             
                self.press_number = 0
                self.current_action = ""
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )
                    
        elif mouse_event.button() == Qt.LeftButton and self.current_action == "draw_rect":
            self.press_number = self.press_number + 1
            if self.press_number == 1:
                self.cursor_coordinates.append( self.cursor_position )
            elif self.press_number == 2: 
                self.cursor_coordinates.append( self.cursor_position ) 
                self.draw_rect( self.cursor_coordinates )             
                self.press_number = 0
                self.current_action = ""
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )  
                    
        elif mouse_event.button() == Qt.LeftButton and self.current_action == "draw_triangle":
            self.press_number = self.press_number + 1
            if self.press_number == 1:
                self.cursor_coordinates.append( self.cursor_position )
            elif self.press_number == 2: 
                self.cursor_coordinates.append( self.cursor_position ) 
            elif self.press_number == 3: 
                self.cursor_coordinates.append( self.cursor_position )               
                self.draw_triangle( self.cursor_coordinates )  
                QApplication.restoreOverrideCursor()
                for item in self.symbol_drawlist_temp:
                    self.removeItem( item )
                self.press_number = 0
                self.current_action = ""
           
    def mouseMoveEvent( self, mouse_event ):
        self.cursor_position = QPoint( mouse_event.scenePos().x(), mouse_event.scenePos().y() )
        if self.press_number == 0 and self.current_action == "draw_arrive_point":
            if len( self.cursor_coordinates ) == 0:
                self.cursor_coordinates.append( self.cursor_position )
            else:
                self.cursor_coordinates[0] = self.cursor_position
                    
            self.removeItem( self.arrive_point )
            self.arrive_point = ArrivePoint( self )
            self.arrive_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
            self.addItem( self.arrive_point )
            self.symbol_drawlist_temp.append( self.arrive_point )
        
        elif self.press_number == 0 and self.current_action == "draw_leave_point":
            if len( self.cursor_coordinates ) == 0:
                self.cursor_coordinates.append( self.cursor_position )
            else:
                self.cursor_coordinates[0] = self.cursor_position
                    
            self.removeItem( self.leave_point )
            self.leave_point = LeavePoint( self )
            self.leave_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
            self.addItem( self.leave_point )
            self.symbol_drawlist_temp.append( self.leave_point )
        
        elif self.press_number == 0 and self.current_action == "draw_tee_point":
            if len( self.cursor_coordinates ) == 0:
                self.cursor_coordinates.append( self.cursor_position )
            else:
                self.cursor_coordinates[0] = self.cursor_position
                    
            self.removeItem( self.tee_point )
            self.tee_point = TeePoint( self )
            self.tee_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
            self.addItem( self.tee_point )
            self.symbol_drawlist_temp.append( self.tee_point )
        
        elif self.press_number == 0 and self.current_action == "draw_spindle_point":
            if len( self.cursor_coordinates ) == 0:
                self.cursor_coordinates.append( self.cursor_position )
            else:
                self.cursor_coordinates[0] = self.cursor_position
                    
            self.removeItem( self.spindle_point )
            self.spindle_point = SpindlePoint( self )
            self.spindle_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
            self.addItem( self.spindle_point )
            self.symbol_drawlist_temp.append( self.spindle_point )
                
        if self.press_number == 1 and self.current_action == "draw_line":
            if len( self.cursor_coordinates ) == 1:
                self.cursor_coordinates.append( self.cursor_position )
                self.line = QGraphicsLineItem( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y(), 
                                               self.cursor_coordinates[1].x(), self.cursor_coordinates[1].y() )
                self.addItem( self.line )
                self.symbol_drawlist_temp.append( self.line )
                                                    
            elif len( self.cursor_coordinates ) == 2:
                self.cursor_coordinates[1] = self.cursor_position
                self.removeItem( self.line )
                self.line = QGraphicsLineItem( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y(), 
                                               self.cursor_coordinates[1].x(), self.cursor_coordinates[1].y() )
                self.addItem( self.line )
                self.symbol_drawlist_temp.append( self.line )
            
        elif self.press_number == 1 and self.current_action == "draw_rect":
            if len( self.cursor_coordinates ) == 1:
                self.cursor_coordinates.append( self.cursor_position )
                                    
            elif len( self.cursor_coordinates ) == 2:
                self.cursor_coordinates[1] = self.cursor_position
                self.removeItem( self.rect )
                
            if self.cursor_coordinates[0].x() <= self.cursor_coordinates[1].x():
                pos_x_left = self.cursor_coordinates[0].x()
                pos_x_right = self.cursor_coordinates[1].x()  
                
            elif self.cursor_coordinates[0].x() > self.cursor_coordinates[1].x():
                pos_x_left = self.cursor_coordinates[1].x()
                pos_x_right = self.cursor_coordinates[0].x()   
                
            if self.cursor_coordinates[0].y() <= self.cursor_coordinates[1].y():
                pos_y_bottom = self.cursor_coordinates[1].y()
                pos_y_top = self.cursor_coordinates[0].y()  
                
            elif self.cursor_coordinates[0].y() > self.cursor_coordinates[1].y():
                pos_y_bottom = self.cursor_coordinates[0].y()
                pos_y_top = self.cursor_coordinates[1].y()  
            
            rect_width = abs( pos_x_right - pos_x_left )
            rect_height = abs( pos_y_bottom - pos_y_top )   
    
            self.rect = QGraphicsRectItem( pos_x_left, pos_y_top, rect_width, rect_height )  
            self.addItem( self.rect )
            self.symbol_drawlist_temp.append( self.rect )   
            
        elif self.press_number == 1 and self.current_action == "draw_triangle":
            if self.press_number == 1 and len( self.cursor_coordinates ) == 1:
                self.cursor_coordinates.append( self.cursor_position )
            elif self.press_number == 1 and len( self.cursor_coordinates ) == 2:
                self.cursor_coordinates[ self.press_number ] = self.cursor_position    
            
            self.removeItem( self.triangle )
            polygon = QPolygonF() 
            for point in self.cursor_coordinates:
                polygon.append( point )
                
            self.triangle = QGraphicsPolygonItem( polygon )  
            self.addItem( self.triangle )
            self.symbol_drawlist_temp.append( self.triangle )   
            
        elif self.press_number == 2 and self.current_action == "draw_triangle":
            if self.press_number == 2 and len( self.cursor_coordinates ) == 2:
                self.cursor_coordinates.append( self.cursor_position )
            elif self.press_number == 2 and len( self.cursor_coordinates ) == 3:
                self.cursor_coordinates[ self.press_number ] = self.cursor_position
            
            self.removeItem( self.triangle )
            polygon = QPolygonF() 
            for point in self.cursor_coordinates:
                polygon.append( point )
                
            self.triangle = QGraphicsPolygonItem( polygon )  
            self.addItem( self.triangle )
            self.symbol_drawlist_temp.append( self.triangle )                               

    def draw_arrive_point( self, positions ):
        arrive_point = ArrivePoint( self )
        arrive_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
        arrive_point.setFlag( QGraphicsItem.ItemIsSelectable )                                                              
        self.addItem( arrive_point )
        self.symbol_drawlist.append( arrive_point )
       
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()       
        
    def draw_leave_point( self, positions ):
        leave_point = LeavePoint( self )
        leave_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
        leave_point.setFlag( QGraphicsItem.ItemIsSelectable )                                                              
        self.addItem( leave_point )
        self.symbol_drawlist.append( leave_point )
       
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()    
        
    def draw_tee_point( self, positions ):
        tee_point = TeePoint( self )
        tee_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
        tee_point.setFlag( QGraphicsItem.ItemIsSelectable )                                                              
        self.addItem( tee_point )
        self.symbol_drawlist.append( tee_point )
       
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()  
        
    def draw_spindle_point( self, positions ):
        spindle_point = SpindlePoint( self )
        spindle_point.setPos( self.cursor_coordinates[0].x(), self.cursor_coordinates[0].y() )
        spindle_point.setFlag( QGraphicsItem.ItemIsSelectable )                                                              
        self.addItem( spindle_point )
        self.symbol_drawlist.append( spindle_point )
       
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()       
            
    def draw_line( self, positions ):
        pen_axis_main = QPen( QColor( 0, 0, 0 ) )
        pen_axis_main.setWidth( 2 )
        pen_axis_main.setStyle( Qt.SolidLine )  
                                 
        line = QGraphicsLineItem(   self.cursor_coordinates[0].x(), 
                                    self.cursor_coordinates[0].y(), 
                                    self.cursor_coordinates[1].x(), 
                                    self.cursor_coordinates[1].y() )
        line.setFlag( QGraphicsItem.ItemIsSelectable )
        line.setPen( pen_axis_main )                                                               
        self.addItem( line )
        self.symbol_drawlist.append( line )
        
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()  
            
    def draw_rect( self, positions ):
        pen_axis_main = QPen( QColor( 0, 0, 0 ) )
        pen_axis_main.setWidth( 2 )
        pen_axis_main.setStyle( Qt.SolidLine )  
                                 
        if self.cursor_coordinates[0].x() < self.cursor_coordinates[1].x():
            pos_x_left = self.cursor_coordinates[0].x()
            pos_x_right = self.cursor_coordinates[1].x()  
            
        elif self.cursor_coordinates[0].x() > self.cursor_coordinates[1].x():
            pos_x_left = self.cursor_coordinates[1].x()
            pos_x_right = self.cursor_coordinates[0].x()   
            
        if self.cursor_coordinates[0].y() < self.cursor_coordinates[1].y():
            pos_y_bottom = self.cursor_coordinates[1].y()
            pos_y_top = self.cursor_coordinates[0].y()  
            
        elif self.cursor_coordinates[0].y() > self.cursor_coordinates[1].y():
            pos_y_bottom = self.cursor_coordinates[0].y()
            pos_y_top = self.cursor_coordinates[1].y()  
            
        rect_width = abs( pos_x_right - pos_x_left )
        rect_height = abs( pos_y_bottom - pos_y_top )   
        
        rect = QGraphicsRectItem( pos_x_left, pos_y_top, rect_width, rect_height )  
        rect.setFlag( QGraphicsItem.ItemIsSelectable )
        rect.setPen( pen_axis_main )                                                               
        self.addItem( rect )
        self.symbol_drawlist.append( rect )
        
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()    
            
    def draw_triangle( self, positions ):
        pen_axis_main = QPen( QColor( 0, 0, 0 ) )
        pen_axis_main.setWidth( 2 )
        pen_axis_main.setStyle( Qt.SolidLine )  
                                 
        polygon = QPolygonF() 
        for point in positions:
            polygon.append( point )
         
        triangle = QGraphicsPolygonItem( polygon ) 
        triangle.setFlag( QGraphicsItem.ItemIsSelectable )
        triangle.setPen( pen_axis_main )                                                               
        self.addItem( triangle )
        self.symbol_drawlist.append( triangle )
        
        self.cursor_coordinates.clear()
        while QApplication.overrideCursor() is not None:
            QApplication.restoreOverrideCursor()  
    
class SkeyEditorDialog(QDialog):
    """"SkeyEditorDialog Window"""
    
    def __init__( self, parent = None ):
        QDialog.__init__(self, parent)
        self.skeys = {}
        self.skeysList = []
        self.sheet_width = 400
        self.sheet_height = 400
        
        self.scales = []

        self.sheet_units_number_x = 20
        self.sheet_units_number_y = 20
        
        self.origin_x = self.sheet_width / 2
        self.origin_y = self.sheet_height / 2
        
        self.zoom = 1
        self.groups = {}
        self.subgroups = {}
                
        self.max_symbol_size = 0
        self.min_symbol_size = 10000
        
        self.unit_size = 500
 
        self.sheet_limits_gap_x = 5
        self.sheet_limits_gap_y = 5
                        
        self.step_x_main = self.sheet_width / self.sheet_units_number_x
        self.step_x_secondary = self.sheet_width / ( self.sheet_units_number_x * 2 )
        
        self.step_y_main = self.sheet_height / self.sheet_units_number_y
        self.step_y_secondary = self.sheet_height / ( self.sheet_units_number_y * 2 )
        
        self.point_diameter = 15
               
        self.iconsLibraryPath = os.path.dirname(os.path.abspath(__file__)).replace( "\lib\omp","\lib\pipecad" ) + "/icons"
        self.symbol_file_json = os.getenv('PIPECAD_SETTINGS_PATH').replace( "\\\\","\\" ) + "\\iso\\IsoSymbolsLibrary.json" 
        
        self.skeys_desc = {}
        self.skeys_desc["BU+D"] = ["Bends" , "180° pulled return bend"]
        self.skeys_desc["BUBW"] = ["Bends" , "180° Pulled return bend with weld at each end"]
        self.skeys_desc["BM**"] = ["Bends" , "Bend"]
        self.skeys_desc["BECL"] = ["Bends" , "Bend with clamped end connections"]
        self.skeys_desc["BEBS"] = ["Bends" , "Bend with flanged ball/socket end connections"]
        self.skeys_desc["BEGF"] = ["Bends" , "Bend with flanged gland-type end connections"]
        self.skeys_desc["BEFA"] = ["Bends" , "Bend with flared end connections"]
        self.skeys_desc["BEGL"] = ["Bends" , "Bend with glued end connections"]
        self.skeys_desc["BEPF"] = ["Bends" , "Bend with push fit connections"]
        self.skeys_desc["L@BW"] = ["Bends" , "Butt Weld Lobster Back Bend"]
        self.skeys_desc["T@BW"] = ["Bends" , "Butt Weld Lobster Back Bend with Tee"]
        self.skeys_desc["MIBW"] = ["Bends" , "Butt weld mitre bend"]
        self.skeys_desc["MTBW"] = ["Bends" , "Butt weld mitre tee bend"]
        self.skeys_desc["BUFL"] = ["Bends" , "Flanged 180° return bend"]
        self.skeys_desc["BEFL"] = ["Bends" , "Flanged Bend"]
        self.skeys_desc["BTFL"] = ["Bends" , "Flanged Bend with Tee"]
        self.skeys_desc["L@FL"] = ["Bends" , "Flanged Lobster Back Bend"]
        self.skeys_desc["T@FL"] = ["Bends" , "Flanged Lobster Back Bend with Tee"]
        self.skeys_desc["MIFL"] = ["Bends" , "Flanged mitre bend"]
        self.skeys_desc["MTFL"] = ["Bends" , "Flanged mitre tee bend"]
        self.skeys_desc["L@PL"] = ["Bends" , "Lobster Back Bend"]
        self.skeys_desc["T@PL"] = ["Bends" , "Lobster Back Bend with Tee"]
        self.skeys_desc["MTPL"] = ["Bends" , "Mitre tee bend with plain ends"]
        self.skeys_desc["MIPL"] = ["Bends" , "Mitred Bend"]
        self.skeys_desc["PB+D"] = ["Bends" , "Pulled Bend"]
        self.skeys_desc["TB+D"] = ["Bends" , "Pulled Bend with Tee"]
        self.skeys_desc["PBBW"] = ["Bends" , "Pulled bend with weld at each end"]
        self.skeys_desc["TBBW"] = ["Bends" , "Pulled tee bend with weld at each end"]
        self.skeys_desc["BTBS"] = ["Bends" , "Tee bend with flanged ball/socket end connections"]
        self.skeys_desc["TBGF"] = ["Bends" , "Tee bend with flanged gland-type end connections"]
        self.skeys_desc["KABW"] = ["Caps" , "Butt Weld Cap"]
        self.skeys_desc["KACL"] = ["Caps" , "Clamped cap"]
        self.skeys_desc["KACP"] = ["Caps" , "Compression cap"]
        self.skeys_desc["KAFL"] = ["Caps" , "Flanged cap"]
        self.skeys_desc["KAFA"] = ["Caps" , "Flared cap"]
        self.skeys_desc["KAGL"] = ["Caps" , "Glued cap"]
        self.skeys_desc["KAPF"] = ["Caps" , "Push fit cap"]
        self.skeys_desc["KASC"] = ["Caps" , "Screwed cap"]
        self.skeys_desc["KASW"] = ["Caps" , "Socket weld cap"]
        self.skeys_desc["CLMP"] = ["Clamped Joints" , "Flared Clamp"]
        self.skeys_desc["CLGY"] = ["Clamped Joints" , "Grayloc-type coupling"]
        self.skeys_desc["CLVT"] = ["Clamped Joints" , "Victaulic (Grooved pipe end type)"]
        self.skeys_desc["CLVR"] = ["Clamped Joints" , "Victaulic (Welded /Forded ring type)"]
        self.skeys_desc["LNSC"] = ["Connectors" , "Grayloc (Female) screwed connector"]
        self.skeys_desc["LNSW"] = ["Connectors" , "Grayloc sockect weld connector"]
        self.skeys_desc["LVBW"] = ["Connectors" , "Victaulic welded ring type"]
        self.skeys_desc["CEBW"] = ["Couplings" , "Butt Weld Elbolet"]
        self.skeys_desc["CPCF"] = ["Couplings" , "Centre Flange"]
        self.skeys_desc["COCP"] = ["Couplings" , "Compression Fitting Coupling"]
        self.skeys_desc["COCL"] = ["Couplings" , "Coupling with clamped end connections"]
        self.skeys_desc["CSCP"] = ["Couplings" , "Coupling with compression sleeve connections"]
        self.skeys_desc["COFA"] = ["Couplings" , "Coupling with flared end connections"]
        self.skeys_desc["COGL"] = ["Couplings" , "Coupling with glued connections"]
        self.skeys_desc["COGY"] = ["Couplings" , "Coupling with Grayloc connections"]
        self.skeys_desc["COPF"] = ["Couplings" , "Coupling with push fit end connections"]
        self.skeys_desc["COVT"] = ["Couplings" , "Coupling with Victaulic connections (Grooved pipe)"]
        self.skeys_desc["COVR"] = ["Couplings" , "Coupling with Victaulic connections (Welded connections)"]
        self.skeys_desc["COSC"] = ["Couplings" , "Screwed Fitting Coupling"]
        self.skeys_desc["CESC"] = ["Couplings" , "Screwed Fitting Elbolet"]
        self.skeys_desc["NRSC"] = ["Couplings" , "Screwed Fitting Nipple"]
        self.skeys_desc["NBSC"] = ["Couplings" , "Screwed Nipple"]
        self.skeys_desc["COSW"] = ["Couplings" , "Socket Weld Coupling"]
        self.skeys_desc["CESW"] = ["Couplings" , "Socket Weld Elbolet"]
        self.skeys_desc["CPWP"] = ["Couplings" , "Watertight Bulkhead and Deck"]
        self.skeys_desc["CPWT"] = ["Couplings" , "Welded Sleeve thru Pipe"]
        self.skeys_desc["CRBW"] = ["Crosses" , "Butt Weld Cross"]
        self.skeys_desc["CRCP"] = ["Crosses" , "Compression Fitting Cross"]
        self.skeys_desc["CR**"] = ["Crosses" , "Cross"]
        self.skeys_desc["CRCL"] = ["Crosses" , "Cross with clamped end connections"]
        self.skeys_desc["CRBS"] = ["Crosses" , "Cross with flanged ball/socket end connections"]
        self.skeys_desc["CRGF"] = ["Crosses" , "Cross with flanged gland-type end connections"]
        self.skeys_desc["CRFA"] = ["Crosses" , "Cross with flared end connections"]
        self.skeys_desc["CRGL"] = ["Crosses" , "Cross with glued end connections"]
        self.skeys_desc["CRPF"] = ["Crosses" , "Cross with push fit end connections"]
        self.skeys_desc["CRFL"] = ["Crosses" , "Flanged Cross"]
        self.skeys_desc["X@"] = ["Crosses" , "Generic Y-type Cross with user-definable out- and off- legs"]
        self.skeys_desc["CRSC"] = ["Crosses" , "Screwed Fitting Cross"]
        self.skeys_desc["CRSO"] = ["Crosses" , "Set-on cross"]
        self.skeys_desc["CYSO"] = ["Crosses" , "Set-on cross (Y-type)"]
        self.skeys_desc["CRRF"] = ["Crosses" , "Set-on reinforced cross"]
        self.skeys_desc["CRSW"] = ["Crosses" , "Socket Weld Cross No"]
        self.skeys_desc["CSSO"] = ["Crosses" , "Stub in cross"]
        self.skeys_desc["CSRF"] = ["Crosses" , "Stub in reinforced cross"]
        self.skeys_desc["CY**"] = ["Crosses" , "Y-type cross"]
        self.skeys_desc["ELBW"] = ["Elbows" , "Butt Weld Elbow"]
        self.skeys_desc["ETBW"] = ["Elbows" , "Butt Weld Elbow with Tee"]
        self.skeys_desc["EUBW"] = ["Elbows" , "Butt Weld Return Elbow"]
        self.skeys_desc["ELCP"] = ["Elbows" , "Compression elbow (90° and 45°)"]
        self.skeys_desc["ETCP"] = ["Elbows" , "Compression Fitting Elbow with Tee"]
        self.skeys_desc["ELCL"] = ["Elbows" , "Elbow with clamped end connections"]
        self.skeys_desc["ELBS"] = ["Elbows" , "Elbow with flanged ball/socket end connections"]
        self.skeys_desc["ELGF"] = ["Elbows" , "Elbow with flanged gland-type end connections"]
        self.skeys_desc["ELFA"] = ["Elbows" , "Elbow with flared end connections"]
        self.skeys_desc["ELGL"] = ["Elbows" , "Elbow with glued end connections"]
        self.skeys_desc["ELPF"] = ["Elbows" , "Elbow with push fit end connections"]
        self.skeys_desc["EUPL"] = ["Elbows" , "Plain end return elbow (180°)"]
        self.skeys_desc["ER"] = ["Elbows" , "Reducing Elbow"]
        self.skeys_desc["ERCL"] = ["Elbows" , "Reducing elbow with clamped end connections"]
        self.skeys_desc["ERFA"] = ["Elbows" , "Reducing elbow with flared end connections"]
        self.skeys_desc["ELSC"] = ["Elbows" , "Screwed elbow with Female ends (90° and 45°)"]
        self.skeys_desc["EBSC"] = ["Elbows" , "Screwed elbow with Male ends (90° and 45°)"]
        self.skeys_desc["ETSC"] = ["Elbows" , "Screwed Fitting Elbow with Tee"]
        self.skeys_desc["ELSW"] = ["Elbows" , "Socket Weld Elbow"]
        self.skeys_desc["ETSW"] = ["Elbows" , "Socket Weld Elbow with Tee"]
        self.skeys_desc["ETCL"] = ["Elbows" , "Teed elbow with clamped end connections"]
        self.skeys_desc["ETFA"] = ["Elbows" , "Teed elbow with flared end connections"]
        self.skeys_desc["ETGL"] = ["Elbows" , "Teed elbow with glued end connections"]
        self.skeys_desc["ETPF"] = ["Elbows" , "Teed elbow with push fit end connections"]
        self.skeys_desc["FY"] = ["Filters" , "‘Y’-type Filter/Strainer"]
        self.skeys_desc["FA**"] = ["Filters" , "Angled Filter"]
        self.skeys_desc["FO**"] = ["Filters" , "Offset Filter"]
        self.skeys_desc["FR**"] = ["Filters" , "Return Filter"]
        self.skeys_desc["FI**"] = ["Filters" , "Straight-Through (In-Line) Filter"]
        self.skeys_desc["TUBE"] = ["Fixed Length Pipes" , "Fixed Length Pipe - to be displayed and stretched, like implied tube on an isometric"]
        self.skeys_desc["FPCL"] = ["Fixed Length Pipes" , "Fixed length pipe with clamped end conditions"]
        self.skeys_desc["FPCP"] = ["Fixed Length Pipes" , "Fixed length pipe with compression end connections"]
        self.skeys_desc["FPFL"] = ["Fixed Length Pipes" , "Fixed length pipe with flanged ball and socket"]
        self.skeys_desc["FPFA"] = ["Fixed Length Pipes" , "Fixed length pipe with flared end connections"]
        self.skeys_desc["FPGL"] = ["Fixed Length Pipes" , "Fixed length pipe with glued end connections"]
        self.skeys_desc["FPPL"] = ["Fixed Length Pipes" , "Fixed Length Pipe with Plain Ends"]
        self.skeys_desc["FPPF"] = ["Fixed Length Pipes" , "Fixed length pipe with push fit end connections"]
        self.skeys_desc["FPSC"] = ["Fixed Length Pipes" , "Fixed length pipe with screwed end connections"]
        self.skeys_desc["FPSW"] = ["Fixed Length Pipes" , "Fixed length pipe with socket end connections"]
        self.skeys_desc["FLBL"] = ["Flanges" , "Blind or Blanking Flange"]
        self.skeys_desc["FLGM"] = ["Flanges" , "Cast/ lined flange with Male gland type"]
        self.skeys_desc["FLFF"] = ["Flanges" , "Cast/lined fixed flange (Female) – Cast/lined flange"]
        self.skeys_desc["FLGF"] = ["Flanges" , "Cast/lined flange with Female gland type"]
        self.skeys_desc["FLFR"] = ["Flanges" , "Cast/lined rotating flange"]
        self.skeys_desc["FC"] = ["Flanges" , "Concentric reducing flange"]
        self.skeys_desc["FE"] = ["Flanges" , "Eccentric reducing flange"]
        self.skeys_desc["FLFL"] = ["Flanges" , "Flared/Loose backing flange"]
        self.skeys_desc["FLGL"] = ["Flanges" , "Glued (Female) connection"]
        self.skeys_desc["JFSO"] = ["Flanges" , "Jacket slip-on flange"]
        self.skeys_desc["JFWN"] = ["Flanges" , "Jacket weld neck flange"]
        self.skeys_desc["FLRG"] = ["Flanges" , "Lap Joint Ring (Loose Backing Flange)"]
        self.skeys_desc["FBSE"] = ["Flanges" , "Lap joint ring/Stub end combined flange"]
        self.skeys_desc["FLSE"] = ["Flanges" , "Lap Joint Stub End (Loose Backing Flange)"]
        self.skeys_desc["FLLB"] = ["Flanges" , "Loose Backing"]
        self.skeys_desc["FOSO"] = ["Flanges" , "Orifice slip-on flange with tapping connection"]
        self.skeys_desc["FOWN"] = ["Flanges" , "Orifice weld neck flange with tapping connections"]
        self.skeys_desc["FLPF"] = ["Flanges" , "Push fit (Female) connection"]
        self.skeys_desc["FLRC"] = ["Flanges" , "Reducing Concentric"]
        self.skeys_desc["FLRE"] = ["Flanges" , "Reducing Eccentric"]
        self.skeys_desc["FLSC"] = ["Flanges" , "Screwed Fitting"]
        self.skeys_desc["FLSF"] = ["Flanges" , "Seal-welded flange (Sarlun/Sargol) (Female) connection"]
        self.skeys_desc["FLSM"] = ["Flanges" , "Seal-welded flange (Sarlun/Sargol) (Male) connection"]
        self.skeys_desc["FLSO"] = ["Flanges" , "Slip-on Flange"]
        self.skeys_desc["FLSJ"] = ["Flanges" , "Slip-on flange with J-type weld"]
        self.skeys_desc["FLSW"] = ["Flanges" , "Socket Weld Flange"]
        self.skeys_desc["FLMP"] = ["Flanges" , "Stub End (LJSE) – use with glued / push fit systems"]
        self.skeys_desc["FLWN"] = ["Flanges" , "Weld Neck Flange"]
        self.skeys_desc["BNUT"] = ["Hygienic Fittings" , "Backing nut"]
        self.skeys_desc["LN"] = ["Hygienic Fittings" , "Backing nut liner"]
        self.skeys_desc["LNBW"] = ["Hygienic Fittings" , "Backing nut liner butt welded"]
        self.skeys_desc["LRBW"] = ["Hygienic Fittings" , "Backing nut reducing liner butt weld"]
        self.skeys_desc["LREX"] = ["Hygienic Fittings" , "Backing nut reducing liner expanded"]
        self.skeys_desc["BP"] = ["Hygienic Fittings" , "Blank plain"]
        self.skeys_desc["BTP"] = ["Hygienic Fittings" , "Blank thermocouple connector"]
        self.skeys_desc["ZB"] = ["Hygienic Fittings" , "Butterfly valve"]
        self.skeys_desc["LCBW"] = ["Hygienic Fittings" , "Clamp liner butt weld"]
        self.skeys_desc["LCEX"] = ["Hygienic Fittings" , "Clamp liner expanded"]
        self.skeys_desc["DVP"] = ["Hygienic Fittings" , "Drain/Vent plug"]
        self.skeys_desc["4D"] = ["Hygienic Fittings" , "Four-port single level valve (D)"]
        self.skeys_desc["4Z"] = ["Hygienic Fittings" , "Four-port single level valve (Z)"]
        self.skeys_desc["IG"] = ["Hygienic Fittings" , "Graduated control valve (D)"]
        self.skeys_desc["ZG"] = ["Hygienic Fittings" , "Graduated control valve (Z)"]
        self.skeys_desc["BM"] = ["Hygienic Fittings" , "Male blanking plug"]
        self.skeys_desc["MPBW"] = ["Hygienic Fittings" , "Male part connector butt weld"]
        self.skeys_desc["MPEX"] = ["Hygienic Fittings" , "Male part connector expanded"]
        self.skeys_desc["ADMF"] = ["Hygienic Fittings" , "Male to Female Adapter"]
        self.skeys_desc["ADMM"] = ["Hygienic Fittings" , "Male-to-male adapter"]
        self.skeys_desc["MD"] = ["Hygienic Fittings" , "Multi-port dual level valve with D spindle"]
        self.skeys_desc["MZ"] = ["Hygienic Fittings" , "Multi-port dual level valve with Z spindle"]
        self.skeys_desc["NV"] = ["Hygienic Fittings" , "Non-return valve"]
        self.skeys_desc["ZV"] = ["Hygienic Fittings" , "Pressure relief valve (Instrument type) (I)"]
        self.skeys_desc["VZ"] = ["Hygienic Fittings" , "Pressure relief valve (Z)"]
        self.skeys_desc["BBC"] = ["Hygienic Fittings" , "Reducing concentric blank boss"]
        self.skeys_desc["BBE"] = ["Hygienic Fittings" , "Reducing eccentric blank boss"]
        self.skeys_desc["DUMY"] = ["Hygienic Fittings" , "Separator for multi-level valve"]
        self.skeys_desc["3D"] = ["Hygienic Fittings" , "Three-port single level valve (D)"]
        self.skeys_desc["3Z"] = ["Hygienic Fittings" , "Three-port single level valve (Z)"]
        self.skeys_desc["K3"] = ["Hygienic Fittings" , "Three-way check valve"]
        self.skeys_desc["2D"] = ["Hygienic Fittings" , "Two-port single level (angle type) valve (D)"]
        self.skeys_desc["2Z"] = ["Hygienic Fittings" , "Two-port single level (angle type) valve (Z)"]
        self.skeys_desc["KV"] = ["Hygienic Fittings" , "Wide-angle cock"]
        self.skeys_desc["C3"] = ["Instruments" , "3-Way Control Valve"]
        self.skeys_desc["C3**"] = ["Instruments" , "3-Way Control Valve"]
        self.skeys_desc["S3**"] = ["Instruments" , "3-Way Control Valve with Square Indicator"]
        self.skeys_desc["C4"] = ["Instruments" , "4-Way Control Valve"]
        self.skeys_desc["C4**"] = ["Instruments" , "4-Way Control Valve"]
        self.skeys_desc["S4**"] = ["Instruments" , "4-Way Control Valve with Square Indicator"]
        self.skeys_desc["CA"] = ["Instruments" , "Angled Control Valve"]
        self.skeys_desc["SA**"] = ["Instruments" , "Angled Control Valve with Square Indicator"]
        self.skeys_desc["IA**"] = ["Instruments" , "Angled Instrument"]
        self.skeys_desc["XA**"] = ["Instruments" , "Angled Pressure Reducing Valve"]
        self.skeys_desc["RA**"] = ["Instruments" , "Angled Relief Valve"]
        self.skeys_desc["CV"] = ["Instruments" , "Control Valve"]
        self.skeys_desc["SV**"] = ["Instruments" , "Control Valve with Square Indicator"]
        self.skeys_desc["IDFL"] = ["Instruments" , "Flanged Instrument with Dial"]
        self.skeys_desc["HA**"] = ["Instruments" , "Hand-operated angled control valve"]
        self.skeys_desc["HV**"] = ["Instruments" , "Hand-operated control valve"]
        self.skeys_desc["H4**"] = ["Instruments" , "Hand-operated four-way control valve"]
        self.skeys_desc["H3**"] = ["Instruments" , "Hand-operated three-way control valve"]
        self.skeys_desc["II**"] = ["Instruments" , "Instrument"]
        self.skeys_desc["IDPL"] = ["Instruments" , "Instrument dial"]
        self.skeys_desc["M3**"] = ["Instruments" , "Motor-operated 3-way control valve"]
        self.skeys_desc["M4**"] = ["Instruments" , "Motor-operated 4-way control valve"]
        self.skeys_desc["MA**"] = ["Instruments" , "Motor-operated angled control valve"]
        self.skeys_desc["MV**"] = ["Instruments" , "Motor-operated control valve"]
        self.skeys_desc["IO**"] = ["Instruments" , "Offset Instrument"]
        self.skeys_desc["OP"] = ["Instruments" , "Orifice plate"]
        self.skeys_desc["XV**"] = ["Instruments" , "Pressure Reducing Instrument valve"]
        self.skeys_desc["RV"] = ["Instruments" , "Relief Valve"]
        self.skeys_desc["RV**"] = ["Instruments" , "Relief/Vent instrument valve"]
        self.skeys_desc["PR"] = ["Instruments" , "Restrictor plate"]
        self.skeys_desc["IR**"] = ["Instruments" , "Return Instrument"]
        self.skeys_desc["DR"] = ["Instruments" , "Rupture Disc"]
        self.skeys_desc["AR01"] = ["Miscellaneous Items" , "Arrow head (dimension line)"]
        self.skeys_desc["AR02"] = ["Miscellaneous Items" , "Arrow head (message line)"]
        self.skeys_desc["FLOR"] = ["Miscellaneous Items" , "Floor Penetration"]
        self.skeys_desc["FLOW"] = ["Miscellaneous Items" , "Flow arrow"]
        self.skeys_desc["INPP"] = ["Miscellaneous Items" , "Insulation symbol"]
        self.skeys_desc["AR04"] = ["Miscellaneous Items" , "Line break"]
        self.skeys_desc["LOPT"] = ["Miscellaneous Items" , "Location point"]
        self.skeys_desc["WALL"] = ["Miscellaneous Items" , "Wall symbol"]
        self.skeys_desc["BA**"] = ["Miscellaneous Pipe Components" , "Block angle"]
        self.skeys_desc["BO"] = ["Miscellaneous Pipe Components" , "Block offset"]
        self.skeys_desc["BR"] = ["Miscellaneous Pipe Components" , "Block return"]
        self.skeys_desc["EX"] = ["Miscellaneous Pipe Components" , "Expansion Bellows"]
        self.skeys_desc["FT"] = ["Miscellaneous Pipe Components" , "Flame Trap"]
        self.skeys_desc["FX"] = ["Miscellaneous Pipe Components" , "Flexible Hose"]
        self.skeys_desc["CH"] = ["Miscellaneous Pipe Components" , "Hose Coupling"]
        self.skeys_desc["XF"] = ["Miscellaneous Pipe Components" , "Multi-part component (fitting)"]
        self.skeys_desc["NC"] = ["Miscellaneous Pipe Components" , "Non-Category Item"]
        self.skeys_desc["PL"] = ["Miscellaneous Pipe Components" , "Plug"]
        self.skeys_desc["RPAD"] = ["Miscellaneous Pipe Components" , "Reinforcing pad"]
        self.skeys_desc["RP"] = ["Miscellaneous Pipe Components" , "Restrictor plate"]
        self.skeys_desc["SG"] = ["Miscellaneous Pipe Components" , "Sight Glass"]
        self.skeys_desc["SP"] = ["Miscellaneous Pipe Components" , "Slip plate"]
        self.skeys_desc["SR"] = ["Miscellaneous Pipe Components" , "Slip ring"]
        self.skeys_desc["SB"] = ["Miscellaneous Pipe Components" , "Spectacle Blind"]
        self.skeys_desc["OB"] = ["Miscellaneous Pipe Components" , "Spectacle blind (open)"]
        self.skeys_desc["TU"] = ["Miscellaneous Pipe Components" , "Tundish (funnel)"]
        self.skeys_desc["UNIV"] = ["Miscellaneous Pipe Components" , "Universal Skey for special fittings"]
        self.skeys_desc["NZFE"] = ["Nozzle" , "End Flanged"]
        self.skeys_desc["NZWE"] = ["Nozzle" , "End Welded"]
        self.skeys_desc["NZFS"] = ["Nozzle" , "Start Flanged"]
        self.skeys_desc["NZWS"] = ["Nozzle" , "Start Welded"]
        self.skeys_desc["LA"] = ["Olets" , "Butt Weld Latrolet"]
        self.skeys_desc["SW"] = ["Olets" , "Butt Weld Sweepolet"]
        self.skeys_desc["ITFL"] = ["Olets" , "Flanged Instrument Tee"]
        self.skeys_desc["LABW"] = ["Olets" , "Latrolet (Butt weld)"]
        self.skeys_desc["LASC"] = ["Olets" , "Latrolet (Screwed)"]
        self.skeys_desc["LASW"] = ["Olets" , "Latrolet (Socket weld)"]
        self.skeys_desc["NISC"] = ["Olets" , "Nipolet (Screwed)"]
        self.skeys_desc["HCSC"] = ["Olets" , "Olet (Half coupling screwed)"]
        self.skeys_desc["HCSW"] = ["Olets" , "Olet (Half coupling socket weld)"]
        self.skeys_desc["NI**"] = ["Olets" , "Plain End Nipolet"]
        self.skeys_desc["TH"] = ["Olets" , "Screwed Fitting Thredolet"]
        self.skeys_desc["HC"] = ["Olets" , "Screwed Half Coupling"]
        self.skeys_desc["SK"] = ["Olets" , "Socket Weld Sockolet"]
        self.skeys_desc["SKSW"] = ["Olets" , "Sockolet (Socket weld)"]
        self.skeys_desc["SWBW"] = ["Olets" , "Sweepolet (Butt weld)"]
        self.skeys_desc["THSC"] = ["Olets" , "Thredolet (Screwed)"]
        self.skeys_desc["WT"] = ["Olets" , "Weldolet"]
        self.skeys_desc["WTBW"] = ["Olets" , "Weldolet (Butt weld)"]
        self.skeys_desc["LPIN"] = ["Penetration Plate Items" , "Locating Pin"]
        self.skeys_desc["PLT2"] = ["Penetration Plate Items" , "Penetration Plate Centre Sections"]
        self.skeys_desc["PLT1"] = ["Penetration Plate Items" , "Penetration Plate End Sections"]
        self.skeys_desc["PF"] = ["Pipe Blocks" , "Fixed Length"]
        self.skeys_desc["PV"] = ["Pipe Blocks" , "Variable Length"]
        self.skeys_desc["CPBW"] = ["Reducers" , "Butt Weld Concentric Reducer"]
        self.skeys_desc["CTBW"] = ["Reducers" , "Butt Weld Concentric Reducer with Tee"]
        self.skeys_desc["EPBW"] = ["Reducers" , "Butt Weld Eccentric Reducer"]
        self.skeys_desc["EXBW"] = ["Reducers" , "Butt Weld Eccentric Reducer with Tee"]
        self.skeys_desc["RCCP"] = ["Reducers" , "Compression Fitting Concentric Reducer"]
        self.skeys_desc["RC**"] = ["Reducers" , "Concentric reducer"]
        self.skeys_desc["CSBW"] = ["Reducers" , "Concentric reducer (Butt weld swaged from pipe)"]
        self.skeys_desc["CZBW"] = ["Reducers" , "Concentric reducer (Fabricated from a plate with a connection)"]
        self.skeys_desc["CZFL"] = ["Reducers" , "Concentric reducer (Fabricated from plate - flanged with a connection)"]
        self.skeys_desc["CPFL"] = ["Reducers" , "Concentric reducer (Fabricated from plate - flanged)"]
        self.skeys_desc["CTFL"] = ["Reducers" , "Concentric reducer (Flanged with a connection)"]
        self.skeys_desc["RBSC"] = ["Reducers" , "Concentric reducer (Screwed bush)"]
        self.skeys_desc["RNSC"] = ["Reducers" , "Concentric reducer (Screwed nipple)"]
        self.skeys_desc["CTSC"] = ["Reducers" , "Concentric reducer (Screwed with a connection)"]
        self.skeys_desc["RBSW"] = ["Reducers" , "Concentric reducer (Socket weld bush)"]
        self.skeys_desc["CTSW"] = ["Reducers" , "Concentric reducer (Socket weld with a connection)"]
        self.skeys_desc["CXFL"] = ["Reducers" , "Concentric reducer (Swaged from pipe - flanged with a connection)"]
        self.skeys_desc["CXBW"] = ["Reducers" , "Concentric reducer (Swaged from pipe with a connection)"]
        self.skeys_desc["CSFL"] = ["Reducers" , "Concentric reducer (Swaged from plate - flange)"]
        self.skeys_desc["RCCL"] = ["Reducers" , "Concentric reducer with clamped end connections"]
        self.skeys_desc["RCFA"] = ["Reducers" , "Concentric reducer with flared end connections"]
        self.skeys_desc["RCGL"] = ["Reducers" , "Concentric reducer with glued end conditions"]
        self.skeys_desc["RCPF"] = ["Reducers" , "Concentric reducer with push fit end connections"]
        self.skeys_desc["CTCL"] = ["Reducers" , "Concentric teed reducer with clamped end connections"]
        self.skeys_desc["CTFA"] = ["Reducers" , "Concentric teed reducer with flared end connections"]
        self.skeys_desc["CTGL"] = ["Reducers" , "Concentric teed reducer with glued end connections"]
        self.skeys_desc["CTPF"] = ["Reducers" , "Concentric teed reducer with push fit end connections"]
        self.skeys_desc["RE**"] = ["Reducers" , "Eccentric reducer"]
        self.skeys_desc["EZFL"] = ["Reducers" , "Eccentric reducer - flanged (Fabricated from plate with a connection)"]
        self.skeys_desc["EXFL"] = ["Reducers" , "Eccentric reducer - flanged (Swaged from pipe with a connection)"]
        self.skeys_desc["ESFL"] = ["Reducers" , "Eccentric reducer - flanged (Swaged from pipe)"]
        self.skeys_desc["EZBW"] = ["Reducers" , "Eccentric reducer (Butt weld fabricated from plate with a connection)"]
        self.skeys_desc["OTBW"] = ["Reducers" , "Eccentric reducer (Butt weld with a connection)"]
        self.skeys_desc["OTFL"] = ["Reducers" , "Eccentric reducer (Flanged with a connection)"]
        self.skeys_desc["OTSC"] = ["Reducers" , "Eccentric reducer (Screwed with a connection)"]
        self.skeys_desc["ESBW"] = ["Reducers" , "Eccentric reducer (Swaged from pipe)"]
        self.skeys_desc["RECL"] = ["Reducers" , "Eccentric reducer with clamped end connections"]
        self.skeys_desc["REFA"] = ["Reducers" , "Eccentric reducer with flared end connections"]
        self.skeys_desc["REGL"] = ["Reducers" , "Eccentric reducer with glued end conditions"]
        self.skeys_desc["REPF"] = ["Reducers" , "Eccentric reducer with push fit end connections"]
        self.skeys_desc["OTCL"] = ["Reducers" , "Eccentric teed reducer with clamped end connections"]
        self.skeys_desc["OTFA"] = ["Reducers" , "Eccentric teed reducer with flared end connections"]
        self.skeys_desc["OTGL"] = ["Reducers" , "Eccentric teed reducer with glued end connections"]
        self.skeys_desc["OTPF"] = ["Reducers" , "Eccentric teed reducer with push fit end connections"]
        self.skeys_desc["REFL"] = ["Reducers" , "Flanged Eccentric Reducer"]
        self.skeys_desc["EPFL"] = ["Reducers" , "Flanged Eccentric Reducer (Fabricated from plate)"]
        self.skeys_desc["RFPL"] = ["Reducers" , "Reducing block"]
        self.skeys_desc["RCSC"] = ["Reducers" , "Screwed Fitting Concentric Reducer"]
        self.skeys_desc["RESC"] = ["Reducers" , "Screwed Fitting Eccentric Reducer"]
        self.skeys_desc["RCSW"] = ["Reducers" , "Socket Weld Concentric Reducer"]
        self.skeys_desc["RF"] = ["Reducers" , "Special Reducing Flange"]
        self.skeys_desc["01SP"] = ["Spindles" , "All"]
        self.skeys_desc["02SP"] = ["Spindles" , "All"]
        self.skeys_desc["03SP"] = ["Spindles" , "All"]
        self.skeys_desc["04SP"] = ["Spindles" , "All"]
        self.skeys_desc["05SP"] = ["Spindles" , "All"]
        self.skeys_desc["06SP"] = ["Spindles" , "All"]
        self.skeys_desc["07SP"] = ["Spindles" , "All"]
        self.skeys_desc["08SP"] = ["Spindles" , "All"]
        self.skeys_desc["09SP"] = ["Spindles" , "All"]
        self.skeys_desc["10SP"] = ["Spindles" , "All"]
        self.skeys_desc["11SP"] = ["Spindles" , "All"]
        self.skeys_desc["12SP"] = ["Spindles" , "All"]
        self.skeys_desc["13SP"] = ["Spindles" , "All"]
        self.skeys_desc["14SP"] = ["Spindles" , "All"]
        self.skeys_desc["15SP"] = ["Spindles" , "All"]
        self.skeys_desc["ANCH"] = ["Supports" , "Anchor"]
        self.skeys_desc["DUCK"] = ["Supports" , "Duck Foot"]
        self.skeys_desc["GUID"] = ["Supports" , "Guide / Steady"]
        self.skeys_desc["01HG"] = ["Supports" , "Hanger"]
        self.skeys_desc["SLVE"] = ["Supports" , "Penetration Sleeve"]
        self.skeys_desc["SKID"] = ["Supports" , "Skid"]
        self.skeys_desc["SPRG"] = ["Supports" , "Spring"]
        self.skeys_desc["TSBW"] = ["Tees" , "Butt Weld Swept Tee"]
        self.skeys_desc["TEBW"] = ["Tees" , "Butt Weld Tee"]
        self.skeys_desc["TSCP"] = ["Tees" , "Compression Fitting Swept Tee"]
        self.skeys_desc["TECP"] = ["Tees" , "Compression Fitting Tee"]
        self.skeys_desc["TSFL"] = ["Tees" , "Flanged Swept Tee"]
        self.skeys_desc["TEFL"] = ["Tees" , "Flanged Tee"]
        self.skeys_desc["Y@"] = ["Tees" , "Generic Y-type Tee with user-definable out- and off- legs"]
        self.skeys_desc["TEGG"] = ["Tees" , "Ghost tee"]
        self.skeys_desc["IT**"] = ["Tees" , "Instrument tee"]
        self.skeys_desc["TORF"] = ["Tees" , "Offset tee (Reinforced set-on)"]
        self.skeys_desc["TTSO"] = ["Tees" , "Offset tee (set-on)"]
        self.skeys_desc["TPUL"] = ["Tees" , "Pulled out tee"]
        self.skeys_desc["TERF"] = ["Tees" , "Reinforced Tee"]
        self.skeys_desc["TESC"] = ["Tees" , "Screwed Fitting Tee"]
        self.skeys_desc["TESO"] = ["Tees" , "Set On Tee"]
        self.skeys_desc["TOSO"] = ["Tees" , "Set-on tangential tee"]
        self.skeys_desc["TYSO"] = ["Tees" , "Set-on Y-type tee"]
        self.skeys_desc["TSSW"] = ["Tees" , "Socket Weld Swept Tee"]
        self.skeys_desc["TESW"] = ["Tees" , "Socket weld tee"]
        self.skeys_desc["TSRF"] = ["Tees" , "Stub in reinforced tee"]
        self.skeys_desc["TSSO"] = ["Tees" , "Stub in tee"]
        self.skeys_desc["TTRF"] = ["Tees" , "Tangential tee (reinforced set-on)"]
        self.skeys_desc["TE**"] = ["Tees" , "Tee"]
        self.skeys_desc["TECL"] = ["Tees" , "Tee with clamped end connections"]
        self.skeys_desc["TEBS"] = ["Tees" , "Tee with flanged ball/socket end connections"]
        self.skeys_desc["TEGF"] = ["Tees" , "Tee with flanged gland-type end connections"]
        self.skeys_desc["TEFA"] = ["Tees" , "Tee with flared end connections"]
        self.skeys_desc["TEGL"] = ["Tees" , "Tee with glued end connections"]
        self.skeys_desc["TEPF"] = ["Tees" , "Tee with push fit end connections"]
        self.skeys_desc["TY**"] = ["Tees" , "Y-type tee"]
        self.skeys_desc["YLRG"] = ["Tees" , "Y-type tee (Large)"]
        self.skeys_desc["YMED"] = ["Tees" , "Y-type tee (Medium)"]
        self.skeys_desc["YSML"] = ["Tees" , "Y-type tee (Small)"]
        self.skeys_desc["TA"] = ["Traps" , "Angled Trap"]
        self.skeys_desc["TI"] = ["Traps" , "In-line Trap"]
        self.skeys_desc["TO"] = ["Traps" , "Offset Trap"]
        self.skeys_desc["TR"] = ["Traps" , "Return Trap"]
        self.skeys_desc["UNSW"] = ["Unions" , "Butt or Socket Weld Union"]
        self.skeys_desc["UNSC"] = ["Unions" , "Screwed Fitting Union"]
        self.skeys_desc["V3**"] = ["Valves" , "3-Way Valve"]
        self.skeys_desc["V4**"] = ["Valves" , "4-Way Valve"]
        self.skeys_desc["AV"] = ["Valves" , "Angled Valve"]
        self.skeys_desc["AV**"] = ["Valves" , "Angled Valve"]
        self.skeys_desc["VB"] = ["Valves" , "Ball Valve"]
        self.skeys_desc["VV"] = ["Valves" , "Basic Valve"]
        self.skeys_desc["CK"] = ["Valves" , "Check Valve"]
        self.skeys_desc["CK**"] = ["Valves" , "Check valve (alternative)"]
        self.skeys_desc["VK"] = ["Valves" , "Cock Valve"]
        self.skeys_desc["VD"] = ["Valves" , "Diaphragm Valve"]
        self.skeys_desc["VT"] = ["Valves" , "Gate Valve"]
        self.skeys_desc["VG"] = ["Valves" , "Globe Valve"]
        self.skeys_desc["VN"] = ["Valves" , "Needle Valve"]
        self.skeys_desc["VP"] = ["Valves" , "Plug Valve"]
        self.skeys_desc["AX**"] = ["Valves" , "Pressure reducing angle valve"]
        self.skeys_desc["AR**"] = ["Valves" , "Relief/Vent angle valve"]
        self.skeys_desc["VR**"] = ["Valves" , "Relief/Vent valve"]
        self.skeys_desc["VS"] = ["Valves" , "Slide Valve"]
        self.skeys_desc["WWA"] = ["Welds" , "Automatic workshop weld"]
        self.skeys_desc["WMSD"] = ["Welds" , "Dotted Erection mitre weld"]
        self.skeys_desc["WFD"] = ["Welds" , "Dotted field fit weld"]
        self.skeys_desc["WMD"] = ["Welds" , "Dotted mitre weld"]
        self.skeys_desc["WMOD"] = ["Welds" , "Dotted Offshore mitre weld"]
        self.skeys_desc["WOD"] = ["Welds" , "Dotted offshore weld"]
        self.skeys_desc["WSD"] = ["Welds" , "Dotted site weld"]
        self.skeys_desc["WWD"] = ["Welds" , "Dotted Workshop Weld"]
        self.skeys_desc["WMS"] = ["Welds" , "Erection mitre weld"]
        self.skeys_desc["WSSR"] = ["Welds" , "Erection seal weld"]
        self.skeys_desc["WOFD"] = ["Welds" , "Field fit offshore dotted"]
        self.skeys_desc["WF"] = ["Welds" , "Field fit weld"]
        self.skeys_desc["WFST"] = ["Welds" , "Field fit weld with shop test requirement"]
        self.skeys_desc["WMFT"] = ["Welds" , "Mitre field fit tack weld"]
        self.skeys_desc["WMF"] = ["Welds" , "Mitre field fit weld"]
        self.skeys_desc["WMT"] = ["Welds" , "Mitre tack weld"]
        self.skeys_desc["WM"] = ["Welds" , "Mitre weld"]
        self.skeys_desc["WVST"] = ["Welds" , "Offshore field fit shop test weld"]
        self.skeys_desc["WOF"] = ["Welds" , "Offshore field fit weld"]
        self.skeys_desc["WMO"] = ["Welds" , "Offshore mitre weld"]
        self.skeys_desc["WOSR"] = ["Welds" , "Offshore seal weld"]
        self.skeys_desc["WOST"] = ["Welds" , "Offshore shop test weld"]
        self.skeys_desc["WO"] = ["Welds" , "Offshore weld"]
        self.skeys_desc["ZTR"] = ["Welds" , "Reinforced trunnion"]
        self.skeys_desc["XXD"] = ["Welds" , "Site socket/screwed compression dotted weld"]
        self.skeys_desc["XX"] = ["Welds" , "Site socket/screwed compression weld"]
        self.skeys_desc["WS"] = ["Welds" , "Site Weld"]
        self.skeys_desc["WSST"] = ["Welds" , "Site workshop test weld"]
        self.skeys_desc["WSSP"] = ["Welds" , "Special site weld (non-spooling)"]
        self.skeys_desc["ZSP*"] = ["Welds" , "Support weld"]
        self.skeys_desc["WFT"] = ["Welds" , "Tack for field fit weld"]
        self.skeys_desc["WOFT"] = ["Welds" , "Tack for offshore field fit weld"]
        self.skeys_desc["WOT"] = ["Welds" , "Tack for offshore weld"]
        self.skeys_desc["WST"] = ["Welds" , "Tack for site weld"]
        self.skeys_desc["ZTN*"] = ["Welds" , "Trunnion weld"]
        self.skeys_desc["WWST"] = ["Welds" , "Workshop shot test weld"]
        self.skeys_desc["WW"] = ["Welds" , "Workshop Weld"]

        self.setupUi()
    
    def setupUi( self ):
        self.setWindowTitle( QT_TRANSLATE_NOOP( "Paragon", "PipeCAD - Iso Symbols Library" ) )
        
        self.groupSkeys = QGroupBox( QT_TRANSLATE_NOOP( "Paragon", "Skeys" ) )
        self.vBoxLaySkeys = QVBoxLayout()
        self.groupSkeys.setLayout(self.vBoxLaySkeys)   
        
        self.groupEditor = QGroupBox( QT_TRANSLATE_NOOP( "Paragon", "Shape" ) )       
        self.hBoxLayEditor = QHBoxLayout()
        self.groupEditor.setLayout(self.hBoxLayEditor)
        self.groupEditor.setMinimumSize( self.sheet_width + 140, self.sheet_height + 100 )
        
        self.groupProperties = QGroupBox( QT_TRANSLATE_NOOP( "Paragon", "Properties" ) ) 
        self.gridProperties = QGridLayout()
        self.groupProperties.setLayout(self.gridProperties)   
        
        self.groupPreview = QGroupBox( QT_TRANSLATE_NOOP( "Paragon", "Preview" ) ) 
        self.vBoxLayPreview = QVBoxLayout()
        self.groupPreview.setLayout( self.vBoxLayPreview )
        
        self.txtSearch = QLineEdit( "" )
        self.txtSearch.setFixedSize( 470, 24 )  
        
        self.btnFilterClear = QPushButton( "" )
        self.btnFilterClear.setToolTip( QT_TRANSLATE_NOOP( "Common", "Clear Filter" ) )
        self.btnFilterClear.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/common/100x100_filter_clear.png' ) ) )
        self.btnFilterClear.setIconSize( QSize( 16, 16 ) )
        self.btnFilterClear.setMinimumSize( 24, 24 )  
        self.btnFilterClear.setMaximumSize( 24, 24 )  
       
        self.btnPlotSelectElement = QPushButton( "" )
        self.btnPlotSelectElement.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Select Element" ) )
        self.btnPlotSelectElement.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/common/128x128_select_element.png' ) ) )
        self.btnPlotSelectElement.setIconSize( QSize( 36, 36 ) )
        self.btnPlotSelectElement.setMinimumSize( 36, 36 )  
        self.btnPlotSelectElement.setMaximumSize( 36, 36 )   
       
        self.btnPlotPointArrive = QPushButton( "" )
        self.btnPlotPointArrive.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Arrive Connection Point" ) )
        self.btnPlotPointArrive.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_point_arrive.png' ) ) )
        self.btnPlotPointArrive.setIconSize( QSize( 36, 36 ) )
        self.btnPlotPointArrive.setMinimumSize( 36, 36 )  
        self.btnPlotPointArrive.setMaximumSize( 36, 36 )  
        
        self.btnPlotPointLeave = QPushButton( "" )
        self.btnPlotPointLeave.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Leave Connection Point" ) )
        self.btnPlotPointLeave.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_point_leave.png' ) ) )
        self.btnPlotPointLeave.setIconSize( QSize( 36, 36 ) )
        self.btnPlotPointLeave.setMinimumSize( 36, 36 )  
        self.btnPlotPointLeave.setMaximumSize( 36, 36 )    
        
        self.btnPlotPointTee = QPushButton( "" )
        self.btnPlotPointTee.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Additional Connection Point" ) )
        self.btnPlotPointTee.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_point_tee.png' ) ) )
        self.btnPlotPointTee.setIconSize( QSize( 36, 36 ) )
        self.btnPlotPointTee.setMinimumSize( 36, 36 )  
        self.btnPlotPointTee.setMaximumSize( 36, 36 )  
        
        self.btnPlotPointSpindle = QPushButton( "" )
        self.btnPlotPointSpindle.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Spindle Connection Point" ) )
        self.btnPlotPointSpindle.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_point_spindle.png' ) ) )
        self.btnPlotPointSpindle.setIconSize( QSize( 36, 36 ) )
        self.btnPlotPointSpindle.setMinimumSize( 36, 36 )  
        self.btnPlotPointSpindle.setMaximumSize( 36, 36 )    
        
        self.btnPlotLine = QPushButton( "" )
        self.btnPlotLine.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Line" ) )
        self.btnPlotLine.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_line.png' ) ) )
        self.btnPlotLine.setIconSize( QSize( 36, 36 ) )
        self.btnPlotLine.setMinimumSize( 36, 36 )  
        self.btnPlotLine.setMaximumSize( 36, 36 )     
        
        self.btnPlotRect = QPushButton( "" )
        self.btnPlotRect.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Rectangle" ) )
        self.btnPlotRect.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_rectangle.png' ) ) )
        self.btnPlotRect.setIconSize( QSize( 36, 36 ) )
        self.btnPlotRect.setMinimumSize( 36, 36 )  
        self.btnPlotRect.setMaximumSize( 36, 36 )     
        
        self.btnPlotTriangle = QPushButton( "" )
        self.btnPlotTriangle.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Triangle" ) )
        self.btnPlotTriangle.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_Triangle.png' ) ) )
        self.btnPlotTriangle.setIconSize( QSize( 36, 36 ) )
        self.btnPlotTriangle.setMinimumSize( 36, 36 )  
        self.btnPlotTriangle.setMaximumSize( 36, 36 )        
        
        self.btnPlotCap = QPushButton( "" )
        self.btnPlotCap.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Dish" ) )
        self.btnPlotCap.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_cap.png' ) ) )
        self.btnPlotCap.setIconSize( QSize( 36, 36 ) )
        self.btnPlotCap.setMinimumSize( 36, 36 )  
        self.btnPlotCap.setMaximumSize( 36, 36 )  
        
        self.btnPlotHexagon = QPushButton( "" )
        self.btnPlotHexagon.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Hexagone" ) )
        self.btnPlotHexagon.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/paragon/128x128_hexagon.png' ) ) )
        self.btnPlotHexagon.setIconSize( QSize( 36, 36 ) )
        self.btnPlotHexagon.setMinimumSize( 36, 36 )  
        self.btnPlotHexagon.setMaximumSize( 36, 36 )  
        
        self.btnClearSheet = QPushButton( "" )
        self.btnClearSheet.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Clear Sheet" ) )
        #<a href="https://www.flaticon.com/free-icons/clean" title="clean icons">Clean icons created by Freepik - Flaticon</a>
        self.btnClearSheet.setIcon( QIcon( os.path.join( self.iconsLibraryPath + '/common/128x128_clear_sheet.png' ) ) )
        self.btnClearSheet.setIconSize( QSize( 30, 30 ) )
        self.btnClearSheet.setMinimumSize( 36, 36 )  
        self.btnClearSheet.setMaximumSize( 36, 36 )  
        
        self.vBoxLayPlotButtons = QVBoxLayout()
        #self.vBoxLayPlotButtons.addWidget(self.btnPlotSelectElement)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotPointArrive)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotPointLeave)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotPointTee)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotPointSpindle)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotLine)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotRect)
        self.vBoxLayPlotButtons.addWidget(self.btnPlotTriangle)
        #self.vBoxLayPlotButtons.addWidget(self.btnPlotCap)
        #self.vBoxLayPlotButtons.addWidget(self.btnPlotHexagon)
        self.vBoxLayPlotButtons.addStretch()
        self.vBoxLayPlotButtons.addWidget(self.btnClearSheet)

        self.treeSkeys = QTreeWidget()
        self.treeSkeys.header().setVisible(False)
        self.treeSkeys.setUniformRowHeights(True)
        self.treeSkeys.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.treeSkeys.customContextMenuRequested.connect(self.customContextMenuRequested)
        
        self.treeRoot = QTreeWidgetItem( self.treeSkeys )
        self.treeRoot.setText( 0, QT_TRANSLATE_NOOP( "Paragon", "Components" ) )
        self.treeRoot.setExpanded(True)

        self.treeSkeys.setMinimumSize( 500, 450 )  
        self.treeSkeys.setMaximumSize( 500, 450 )  
                 
        self.btnImportFromASCII = QPushButton( QT_TRANSLATE_NOOP( "Paragon", "Import from ASCII" ) )
        self.btnImportFromASCII.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Import of Skeys from ASCII file ( Intergraph )" ) )
        self.btnImportFromASCII.setMinimumSize( 248, 28 )  
        self.btnImportFromASCII.setMaximumSize( 248, 28 )   
        
        self.btnImportFromIDF = QPushButton( QT_TRANSLATE_NOOP( "Paragon", "Import from IDF" ) )
        self.btnImportFromIDF.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Import Skeys from IDF file ( AVEVA )" ) )
        self.btnImportFromIDF.setMinimumSize( 248, 28 )  
        self.btnImportFromIDF.setMaximumSize( 248, 28 )  
        
        self.scene = SheetLayout( self )
        self.scene.setSceneRect( - 40, 0, self.sheet_width + 70, self.sheet_height )
                
        self.viewEditor = QGraphicsView( self.scene, self )
        self.viewEditor.setMouseTracking( True )
        self.viewEditor.setRenderHint( QPainter.Antialiasing )
        self.viewEditor.viewport().installEventFilter( self )
                
        self.lblSkey = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Skey" ) )
        self.lblSkey.setMinimumSize( 100, 24 )
        self.lblSkey.setMaximumSize( 100, 24 )
        self.txtSkey = QLineEdit( "" )
        self.txtSkey.setMinimumSize( 250, 24 )
        self.txtSkey.setMaximumSize( 250, 24 )   
               
        self.lblSkeyGroup = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Group" ) )
        self.cbSkeyGroup = QComboBox()
        self.cbSkeyGroup.setMinimumSize( 250, 24 )
        self.cbSkeyGroup.setMaximumSize( 250, 24 )
        self.cbSkeyGroup.setDuplicatesEnabled( False )
        
        self.cbSkeyGroup.addItem( " " ) 
        
        self.lblSkeySubgroup = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Subgroup" ) )
        self.cbSkeySubgroup = QComboBox()
        self.cbSkeySubgroup.setMinimumSize( 250, 24 )
        self.cbSkeySubgroup.setMaximumSize( 250, 24 )
        
        self.cbSkeySubgroup.addItem( " " ) 
        
        self.lblSkeyDesc = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Description" ) )
        self.txtSkeyDesc = QLineEdit( "" )
        self.txtSkeyDesc.setMinimumSize( 250, 24 )
        self.txtSkeyDesc.setMaximumSize( 250, 24 )
        
        self.lblSpindleSkey = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Spindle Skey" ) )
        self.lblSpindleSkey.setWordWrap( True )
        self.cbSpindleSkey = QComboBox()
        self.cbSpindleSkey.setMinimumSize( 130, 24 )
        self.cbSpindleSkey.setMaximumSize( 130, 24 )
        self.cbSpindleSkey.setIconSize( QSize( 24, 24 ) )
        
        icon_SP01 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_01SP.png' ) )
        icon_SP02 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_02SP.png' ) )
        icon_SP03 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_03SP.png' ) )
        icon_SP04 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_04SP.png' ) )
        icon_SP05 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_05SP.png' ) )
        icon_SP06 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_06SP.png' ) )
        icon_SP07 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_07SP.png' ) )
        icon_SP08 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_08SP.png' ) )
        icon_SP09 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_09SP.png' ) )
        icon_SP10 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_10SP.png' ) )
        icon_SP11 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_11SP.png' ) )
        icon_SP12 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_12SP.png' ) )
        icon_SP13 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_13SP.png' ) )
        icon_SP14 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_14SP.png' ) )
        icon_SP15 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_15SP.png' ) )
        icon_SP16 = QIcon( os.path.join( self.iconsLibraryPath + '/paragon/spindles/128x128_16SP.png' ) )
        
        self.cbSpindleSkey.addItem( " " )
        self.cbSpindleSkey.addItem( icon_SP01, "01SP" )
        self.cbSpindleSkey.addItem( icon_SP02, "02SP" )
        self.cbSpindleSkey.addItem( icon_SP03, "03SP" )
        self.cbSpindleSkey.addItem( icon_SP04, "04SP" )
        self.cbSpindleSkey.addItem( icon_SP05, "05SP" )
        self.cbSpindleSkey.addItem( icon_SP06, "06SP" )
        self.cbSpindleSkey.addItem( icon_SP07, "07SP" )
        self.cbSpindleSkey.addItem( icon_SP08, "08SP" )
        self.cbSpindleSkey.addItem( icon_SP09, "09SP" )
        self.cbSpindleSkey.addItem( icon_SP10, "10SP" )
        self.cbSpindleSkey.addItem( icon_SP11, "11SP" )
        self.cbSpindleSkey.addItem( icon_SP12, "12SP" )
        self.cbSpindleSkey.addItem( icon_SP13, "13SP" )
        self.cbSpindleSkey.addItem( icon_SP14, "14SP" )
        self.cbSpindleSkey.addItem( icon_SP15, "15SP" )
        self.cbSpindleSkey.addItem( icon_SP16, "16SP" )
        
        self.btnSpindleSkeyRotateMinus = QPushButton( "-" )
        self.btnSpindleSkeyRotateMinus.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Hexagone" ) )
        self.btnSpindleSkeyRotateMinus.setMinimumSize( 24, 24 )  
        self.btnSpindleSkeyRotateMinus.setMaximumSize( 24, 24 )   

        self.txtSpindleSkeyAngle = QLineEdit( "0°" )
        self.txtSpindleSkeyAngle.setAlignment( Qt.AlignCenter )
        self.txtSpindleSkeyAngle.setMinimumSize( 50, 24 )
        self.txtSpindleSkeyAngle.setMaximumSize( 50, 24 )

        self.btnSpindleSkeyRotatePlus = QPushButton( "+" )
        self.btnSpindleSkeyRotatePlus.setToolTip( QT_TRANSLATE_NOOP( "Paragon", "Draw Hexagone" ) )
        self.btnSpindleSkeyRotatePlus.setMinimumSize( 24, 24 )  
        self.btnSpindleSkeyRotatePlus.setMaximumSize( 24, 24 ) 
        
        self.hBoxLaySpindle = QHBoxLayout()
        self.hBoxLaySpindle.addWidget( self.cbSpindleSkey )   
        self.hBoxLaySpindle.addStretch()          
        #self.hBoxLaySpindle.addWidget( self.btnSpindleSkeyRotateMinus )    
        #self.hBoxLaySpindle.addWidget( self.txtSpindleSkeyAngle )    
        #self.hBoxLaySpindle.addWidget( self.btnSpindleSkeyRotatePlus )    
 
        self.lblScale = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Scale" ) )
        self.txtScale = QLineEdit( "" )
        self.txtScale.setMinimumSize( 250, 24 )
        self.txtScale.setMaximumSize( 250, 24 )
        
        self.lblOrientation = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Orientation" ) )
        self.cbOrientation = QComboBox()
        self.cbOrientation.setMinimumSize( 250, 24 )
        self.cbOrientation.setMaximumSize( 250, 24 )
        
        self.cbOrientation.addItem( QT_TRANSLATE_NOOP( "Paragon", "Use on symmetrical component" ) )
        self.cbOrientation.addItem( QT_TRANSLATE_NOOP( "Paragon", "Use on non-symmetrical component" ) )
        self.cbOrientation.addItem( QT_TRANSLATE_NOOP( "Paragon", "Use on reducers" ) )
        self.cbOrientation.addItem( QT_TRANSLATE_NOOP( "Paragon", "Use on flanges" ) )
        
        self.lblFlowArrow = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Flow Arrow" ) )
        self.lblFlowArrow.setWordWrap( True )
        self.cbFlowArrow = QComboBox()
        self.cbFlowArrow.setMinimumSize( 250, 24 )
        self.cbFlowArrow.setMaximumSize( 250, 24 )
        
        self.cbFlowArrow.addItem( QT_TRANSLATE_NOOP( "Common", "Default" ) )
        self.cbFlowArrow.addItem( QT_TRANSLATE_NOOP( "Common", "Off" ) )
        self.cbFlowArrow.addItem( QT_TRANSLATE_NOOP( "Common", "On" ) )
                          
        self.lblDimensioned = QLabel( QT_TRANSLATE_NOOP( "Paragon", "Dimensioned" ) )
        self.lblDimensioned.setWordWrap( True )
        self.cbDimensioned = QComboBox()
        self.cbDimensioned.setMinimumSize( 250, 24 )
        self.cbDimensioned.setMaximumSize( 250, 24 )
        
        self.cbDimensioned.addItem( QT_TRANSLATE_NOOP( "Common", "Default" ) )
        self.cbDimensioned.addItem( QT_TRANSLATE_NOOP( "Common", "Off" ) )
        self.cbDimensioned.addItem( QT_TRANSLATE_NOOP( "Common", "On" ) )
        
        self.scenePreview = QGraphicsScene( self )
        self.scenePreview.setSceneRect( 0, 0, 150, 170 )
                
        self.viewPreview = QGraphicsView( self.scenePreview, self )
        self.viewPreview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewPreview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.viewPreview.setRenderHint(QPainter.Antialiasing)

        self.vBoxLayPreview.addWidget( self.viewPreview )
        
        self.btnSave = QPushButton( QT_TRANSLATE_NOOP( "Common", "Save Changes to Skey File" ) )
        self.btnSave.setToolTip( QT_TRANSLATE_NOOP( "Common", "Save Changes to Skey File" ) )
        self.btnSave.setMinimumSize( 337, 24 ) 
        self.btnSave.setMaximumSize( 337, 24 ) 
        
        self.gridProperties.addWidget( self.lblSkey, 0, 0 )
        self.gridProperties.addWidget( self.txtSkey, 0, 1 )
        self.gridProperties.addWidget( self.lblSkeyGroup, 1, 0 )
        self.gridProperties.addWidget( self.cbSkeyGroup, 1, 1 )
        self.gridProperties.addWidget( self.lblSkeySubgroup, 2, 0 )
        self.gridProperties.addWidget( self.cbSkeySubgroup, 2, 1 )
        self.gridProperties.addWidget( self.lblSkeyDesc, 3, 0 )
        self.gridProperties.addWidget( self.txtSkeyDesc, 3, 1 )
        self.gridProperties.addWidget( self.lblSpindleSkey, 4, 0 )
        self.gridProperties.addLayout( self.hBoxLaySpindle, 4, 1 )
        self.gridProperties.addWidget( self.lblScale, 5, 0 )
        self.gridProperties.addWidget( self.txtScale, 5, 1 )
        self.gridProperties.addWidget( self.lblOrientation, 6, 0 )
        self.gridProperties.addWidget( self.cbOrientation, 6, 1 )
        self.gridProperties.addWidget( self.lblFlowArrow, 7, 0 )
        self.gridProperties.addWidget( self.cbFlowArrow, 7, 1 )
        self.gridProperties.addWidget( self.lblDimensioned, 8, 0 )
        self.gridProperties.addWidget( self.cbDimensioned, 8, 1 )
        #self.gridProperties.addWidget( self.groupPreview, 9, 0, 1, 2 )
        #self.gridProperties.addWidget( self.btnSave, 9, 0, 1, 2 )

        self.gridProperties.setRowStretch( self.gridProperties.rowCount(), 1)
        self.gridProperties.setColumnStretch( self.gridProperties.columnCount(), 1)
        
        self.hBoxLayFilter = QHBoxLayout()
        self.hBoxLayFilter.addWidget(self.txtSearch)
        self.hBoxLayFilter.addWidget(self.btnFilterClear)
        
        self.vBoxLaySkeys.addLayout(self.hBoxLayFilter)
        self.vBoxLaySkeys.addWidget(self.treeSkeys)
        
        self.hBoxLayImportButtons = QHBoxLayout()
        self.hBoxLayImportButtons.addWidget( self.btnImportFromASCII )
        self.hBoxLayImportButtons.addWidget( self.btnImportFromIDF )
        self.vBoxLaySkeys.addLayout( self.hBoxLayImportButtons )
        self.vBoxLaySkeys.addStretch()
        
        self.hBoxLayMain = QHBoxLayout( self )
        self.hBoxLayMain.addWidget(self.groupSkeys)
        self.hBoxLayMain.addWidget(self.groupEditor)
        self.hBoxLayMain.addWidget(self.groupProperties)
        
        #TODO: self.hBoxLayEditor.addLayout(self.vBoxLayPlotButtons)
        self.hBoxLayEditor.addWidget(self.viewEditor)
        self.hBoxLayEditor.addStretch()
        
        self.vBoxLayMain = QVBoxLayout( self )
        self.vBoxLayMain.addLayout(self.hBoxLayMain)
        
        self.treeSkeys.itemSelectionChanged.connect(self.currentSkeyChanged)
        self.btnImportFromASCII.clicked.connect(self.callImportSkeyFromASCII)
        self.btnImportFromIDF.clicked.connect(self.callImportSkeyFromIDF)
        
        self.cbSkeyGroup.currentTextChanged.connect(self.currentSkeyGroupChanged)
        self.txtSearch.textChanged.connect(self.callFilter)
        self.btnFilterClear.clicked.connect(self.callFilterClear)
        
        self.btnPlotSelectElement.clicked.connect(self.callDrawSelectElement)
        self.btnPlotPointArrive.clicked.connect(self.callDrawArrivePoint)
        self.btnPlotPointLeave.clicked.connect(self.callDrawLeavePoint)
        self.btnPlotPointTee.clicked.connect(self.callDrawTeePoint)
        self.btnPlotPointSpindle.clicked.connect(self.callDrawSpindlePoint)
        self.btnPlotLine.clicked.connect(self.callDrawLine)
        self.btnPlotRect.clicked.connect(self.callDrawRectangle)
        self.btnPlotTriangle.clicked.connect(self.callDrawTriangle)
        self.btnClearSheet.clicked.connect(self.callClearSheet)
        self.btnSpindleSkeyRotateMinus.clicked.connect(self.callSpindleAngleChangeMinus)
        self.btnSpindleSkeyRotatePlus.clicked.connect(self.callSpindleAngleChangePlus)
        self.btnSave.clicked.connect(self.callSave)
        
        self.scene.focusItemChanged.connect(self.focusItemChanged)
                
        self.groupPreview.setEnabled( False )
        self.btnPlotSelectElement.setEnabled( False )
                
        file_exists = os.path.isfile( self.symbol_file_json )
        if file_exists:
            self.callLoadFromJson()
            self.callLoadSkeyTree()
        #self.callReadSkeyASCIIFile()
        #self.callSaveToJson()
        
    def callSpindleAngleChangeMinus( self ):
        self.txtSpindleSkeyAngle.text = str( int( self.txtSpindleSkeyAngle.text[:len( self.txtSpindleSkeyAngle.text ) - 1] ) - 1 ) + "°"
        
    def callSpindleAngleChangePlus( self ):
        self.txtSpindleSkeyAngle.text = str( int( self.txtSpindleSkeyAngle.text[:len( self.txtSpindleSkeyAngle.text ) - 1] ) + 1 ) + "°"
    
    def callDrawSelectElement( self ):
        print( "select element" )
            
    
    def focusItemChanged(self, newItem, oldItem, reason):
        if newItem and reason == Qt.MouseFocusReason:
            print('item {} clicked!'.format(newItem))
            
    def callClearSheet( self ):
        for item in self.scene.symbol_drawlist:
            self.scene.removeItem( item )
 
    def callDrawArrivePoint( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action = "draw_arrive_point"
      
    def callDrawLeavePoint( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action = "draw_leave_point"
            
    def callDrawTeePoint( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action  = "draw_tee_point"   
        
    def callDrawSpindlePoint( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action  = "draw_spindle_point"
            
    def callDrawLine( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action = "draw_line"
                
    def callDrawRectangle( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action = "draw_rect"

    def callDrawTriangle( self ):
        QApplication.restoreOverrideCursor()
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.scene.current_action = "draw_triangle"

    def callFilter( self ):
        self.treeSkeys.clear()

        self.treeRoot = QTreeWidgetItem( self.treeSkeys )
        self.treeRoot.setText( 0, QT_TRANSLATE_NOOP( "Paragon", "Components" ) )
        self.treeRoot.setExpanded( True )
        
        check_value = self.txtSearch.text.upper()
        temp_skey_group = {}
        
        if self.groups != {}:
            for skey_group in self.groups.keys():
                for skey_subgroup in self.groups[ skey_group ].keys():
                    for skey in self.groups[ skey_group ][ skey_subgroup ]:
                        if skey.upper().find( check_value ) > - 1 or skey_subgroup.upper().find( check_value ) > - 1 or skey_group.upper().find( check_value ) > - 1: 
                            if skey_group in temp_skey_group.keys():
                                if skey_subgroup in temp_skey_group[skey_group].keys():
                                    temp_skey_group[skey_group][skey_subgroup].append(skey)
                                else:
                                    temp_skey_group[skey_group][skey_subgroup] = []
                                    temp_skey_group[skey_group][skey_subgroup].append(skey)
                            else:
                                temp_skey_group[skey_group] = {}
                                temp_skey_group[skey_group][skey_subgroup] = []
                                temp_skey_group[skey_group][skey_subgroup].append(skey)
                            
            for skey_group in temp_skey_group.keys():
                group_level = QTreeWidgetItem( self.treeRoot )
                group_level.setExpanded(True)
                group_level.setText( 0, skey_group )
                aIcon = QIcon( ":/PipeCad/Resources/" + skey_group[:4].upper().replace("CAPS","CAP") + ".png" )
                if aIcon.availableSizes() == ():
                    aIcon = QIcon( ":/PipeCad/Resources/MISC.png" )
                group_level.setIcon(0, aIcon )
            
                for skey_subgroup in temp_skey_group[ skey_group ].keys():
                    subgroup_level = QTreeWidgetItem( group_level )
                    subgroup_level.setExpanded(True)
                    subgroup_level.setText( 0, skey_subgroup )
                    for skey in temp_skey_group[ skey_group ][ skey_subgroup ]:
                        skey_level = QTreeWidgetItem( subgroup_level )
                        skey_level.setText( 0, skey )
                    subgroup_level.sortChildren( 0, Qt.AscendingOrder )
            print(group_level.children())
            group_level.sortChildren( 0, Qt.AscendingOrder )


    def callFilterClear( self ):
        self.treeSkeys.clear()
        self.txtSearch.clear()
        
        self.treeRoot = QTreeWidgetItem( self.treeSkeys )
        self.treeRoot.setText( 0, QT_TRANSLATE_NOOP( "Paragon", "Components" ) )
        self.treeRoot.setExpanded(True)
        
        for skey_group in self.groups.keys():
            group_level = QTreeWidgetItem( self.treeRoot )
            group_level.setExpanded(False)
            group_level.setText( 0, skey_group )
            aIcon = QIcon( ":/PipeCad/Resources/" + skey_group[:4].upper().replace("CAPS","CAP") + ".png" )
            if aIcon.availableSizes() == ():
                aIcon = QIcon( ":/PipeCad/Resources/MISC.png" )
            group_level.setIcon(0, aIcon )
                
            for skey_subgroup in self.groups[ skey_group ].keys():
                subgroup_level = QTreeWidgetItem( group_level )
                subgroup_level.setExpanded( False )
                subgroup_level.setText( 0, skey_subgroup )
                for skey in self.groups[ skey_group ][ skey_subgroup ]:
                    skey_level = QTreeWidgetItem( subgroup_level )
                    skey_level.setText( 0, skey )
                subgroup_level.sortChildren( 0, Qt.AscendingOrder )
        group_level.sortChildren( 0, Qt.AscendingOrder )
                
    def currentSkeyGroupChanged( self ):
        self.cbSkeySubgroup.clear()
        self.cbSkeySubgroup.addItem( " " )
        if self.cbSkeyGroup.currentText != " " and self.cbSkeyGroup.currentText != "":
            for subgroup in self.groups[ self.cbSkeyGroup.currentText ]:
                self.cbSkeySubgroup.addItem( subgroup )
            self.cbSkeySubgroup.model().sort(0)

    def currentSkeyChanged( self ):
        self.callClearSheet()
        self.scene.set_grid_center = "Center"
        self.scene.symbol_drawlist = []
        
        self.cbSkeyGroup.setCurrentText( " " )
        self.cbSkeySubgroup.setCurrentText( " " )
        self.txtScale.text = " "
        
        current_level_element = self.treeSkeys.currentItem()
        current_level = 0
        for i in range( 0, 3 ):
            if current_level_element.parent() is not None:
                current_level_element = current_level_element.parent()
                current_level = current_level + 1

        if current_level == 3: 
            selected_skey = self.treeSkeys.currentItem().text(0)
            selected_group = self.skeys[ selected_skey ][ "group" ]
            selected_subgroup = self.skeys[ selected_skey ][ "subgroup" ]
            
            self.txtSkey.text = selected_skey
            self.txtSkeyDesc.text = self.skeys[ selected_skey ][ "description" ]
            
            self.cbSkeyGroup.setCurrentText( selected_group )
            self.cbSkeySubgroup.clear()
            for subgroup in self.groups[ selected_group ].keys():
                self.cbSkeySubgroup.addItem( subgroup )
               
            self.cbSkeySubgroup.model().sort(0)
            self.cbSkeySubgroup.setCurrentText( selected_subgroup )  
    
            if self.skeys[ selected_skey ]["spindle_skey"] == "":
                self.cbSpindleSkey.setCurrentText( " " )  
            else: 
                self.cbSpindleSkey.setCurrentText( self.skeys[ selected_skey ]["spindle_skey"] ) 
                
            self.txtScale.text = self.skeys[ selected_skey ]["scale_factor"]
            self.cbOrientation.setCurrentIndex( self.skeys[ selected_skey ]["orientation"]  ) 
            self.cbFlowArrow.setCurrentIndex( self.skeys[ selected_skey ]["flow_arrow"]  ) 
            self.cbDimensioned.setCurrentIndex( self.skeys[ selected_skey ]["dimensioned"]  ) 
            for item in self.skeys[ selected_skey ]["geometry"]:
                if item.split(":")[0] == "ArrivePoint":
                    x0 = round( float( item.split(":")[1].split(" ")[1].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y0 = round( float( item.split(":")[1].split(" ")[2].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    element = ArrivePoint()
                    element.setPos( x0, y0 )
                    self.scene.addItem( element )
                    self.scene.symbol_drawlist.append( element )
                elif item.split(":")[0] == "LeavePoint":
                    x0 = round( float( item.split(":")[1].split(" ")[1].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y0 = round( float( item.split(":")[1].split(" ")[2].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    element = LeavePoint()
                    element.setPos( x0, y0 )
                    self.scene.addItem( element )
                    self.scene.symbol_drawlist.append( element )
                elif item.split(":")[0] == "TeePoint":
                    x0 = round( float( item.split(":")[1].split(" ")[1].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y0 = round( float( item.split(":")[1].split(" ")[2].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    element = TeePoint()
                    element.setPos( x0, y0 )
                    self.scene.addItem( element )
                    self.scene.symbol_drawlist.append( element )
                elif item.split(":")[0] == "SpindlePoint":
                    x0 = round( float( item.split(":")[1].split(" ")[1].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y0 = round( float( item.split(":")[1].split(" ")[2].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    element = SpindlePoint()
                    element.setPos( x0, y0 )
                    self.scene.addItem( element )
                    self.scene.symbol_drawlist.append( element )
                elif item.split(":")[0] == "Line":
                    x1 = round( float( item.split(":")[1].split(" ")[1].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y1 = round( float( item.split(":")[1].split(" ")[2].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    x2 = round( float( item.split(":")[1].split(" ")[3].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y2 = round( float( item.split(":")[1].split(" ")[4].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    element = QGraphicsLineItem( x1, y1, x2, y2 )
                    self.scene.addItem( element )
                    self.scene.symbol_drawlist.append( element )
                elif item.split(":")[0] == "Rectangle":
                    x0 = round( float( item.split(":")[1].split(" ")[1].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    y0 = round( float( item.split(":")[1].split(" ")[2].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    width = round( float( item.split(":")[1].split(" ")[3].split("=")[1] ), 3 ) * 100.0 + self.origin_x
                    height = round( float( item.split(":")[1].split(" ")[4].split("=")[1] ), 3 ) * 100.0 + self.origin_y
                    element = QGraphicsLineItem( x0, y0, width, height )
                    self.scene.addItem( element )
                    self.scene.symbol_drawlist.append( element )

                
                #    
                #    self.skeys[ self.txtSkey.text ]["geometry"].append( "Line: x1=" + str( x1 ) + " y1=" + str( y1 ) + " x2=" + str( x2 ) + " y2=" + str( y2 ) )
                #elif type( item ) == QGraphicsRectItem:
                #    #x = round ( ( item.rect().x() - self.scene.sheet_width / 2 ) / self.scene.step_x / 20 , 2 ) 
                #    #y = round ( ( item.rect().y() - self.scene.sheet_height / 2 ) / self.scene.step_y / 20 , 2 )
                #    x = self.scene.convert_to_relative_position( QPointF( item.rect().x(), item.rect().y() ) ).x()
                #    y = self.scene.convert_to_relative_position( QPointF( item.rect().x(), item.rect().y() ) ).y() 
                #    width = round ( item.rect().width() / self.scene.step_x / 20 , 2 )
                #    height = round ( item.rect().height() / self.scene.step_x / 20 , 2 )
                #    self.skeys[ self.txtSkey.text ]["geometry"].append(  "Rectangle: x0=" + str( x ) + " y0=" + str( y ) + " width=" + str( width ) + "Height=" + str( height ) )
                #elif type( item ) == QGraphicsPolygonItem:
                #    polygon_geometry = ""
                #    index = 1
                #    for point in item.polygon().toList():
                #        #point_x = round ( ( point.x() - self.scene.sheet_width / 2 ) / self.scene.step_x / 20 , 2 ) 
                #        #point_y = round ( ( point.y() - self.scene.sheet_height / 2 ) / self.scene.step_y / 20 , 2 )
                #        point_x = self.scene.convert_to_relative_position( point ).x()
                #        point_y = self.scene.convert_to_relative_position( point ).y()
                #        polygon_geometry = polygon_geometry + " x" + str( index ) + "=" + str( point_x ) + " y" + str( index ) + "=" + str( point_y )  
                #        index = index + 1
                #
                    
    def callConvertGraphics( self, skey, scale_factor, geometry ):
        start_point_x = ""
        start_point_y = ""
        end_point_x = ""
        start_point_y = ""
        symbol_width = 0
        symbol_height = 0
        new_geometry = []
        scale = 1
        max_size = 1
        max_width = 1
        max_height = 1
        min_width = 10000
        min_height = 10000
        point_arrive = False 
        point_leave = False 

        pen_arrive = QPen( QColor( 51, 51, 255 ) )
        pen_arrive.setWidth( 2 )
        pen_arrive.setStyle( Qt.SolidLine )   
        
        brush_arrive = QBrush( QColor( 51, 51, 255 ) )

        pen_leave = QPen( QColor( 255, 0, 0 ) )
        pen_leave.setWidth( 2 )
        pen_leave.setStyle( Qt.SolidLine )   

        brush_leave = QBrush( QColor( 255, 0, 0 ) )
        
        pen_tee = QPen( Qt.magenta )
        pen_tee.setWidth( 2 )
        pen_tee.setStyle( Qt.SolidLine )   

        brush_tee = QBrush( Qt.magenta )
        
        pen_spindle = QPen( QColor( 111, 0, 0 ) )
        pen_spindle.setWidth( 2 )
        pen_spindle.setStyle( Qt.SolidLine )

        brush_spindle = QBrush( QColor( 111, 0, 0 ) )     

        pen_symbol = QPen( QColor( 26, 26, 26 ) )
        pen_symbol.setWidth( 2 )
        pen_symbol.setStyle( Qt.SolidLine )   
                
        self.scene.set_grid_center()
        
        for x in range( 0, len( geometry ), 3 ):
            if geometry[x] == "1":
                start_point_x = float( geometry[x + 1] )
                start_point_y = float( geometry[x + 2] )
                min_width = min( start_point_x, min_width  )
                min_height = min( start_point_y, min_height  )
                max_width = max( start_point_x, max_width  )
                max_height = max( start_point_y, max_height  )
                
            elif geometry[x] == "2":
                end_point_x = float( geometry[x + 1] )
                end_point_y = float( geometry[x + 2] )
                min_width = min( end_point_x, min_width  )
                min_height = min( end_point_y, min_height  )
                max_width = max( end_point_x, max_width  )
                max_height = max( end_point_y, max_height  )
                
            elif geometry[x] == "3":
                start_point_x = float( geometry[x + 1] )
                start_point_y = float( geometry[x + 2] )
                min_width = min( start_point_x, min_width  )
                min_height = min( start_point_y, min_height  )
                max_width = max( start_point_x, max_width  )
                max_height = max( start_point_y, max_height  )
                
            elif geometry[x] == "6":
                start_point_x = float( geometry[x + 1] )
                start_point_y = float( geometry[x + 2] )
                min_width = min( start_point_x, min_width  )
                min_height = min( start_point_y, min_height  )
                max_width = max( start_point_x, max_width  )
                max_height = max( start_point_y, max_height  )
                
        min_size = min( ( max_width - min_width ) * scale_factor, ( max_height - min_height ) * scale_factor )
        max_size = max( ( max_width - min_width ) * scale_factor, ( max_height - min_height ) * scale_factor )
        
        if max_size <= self.unit_size:
            scale = scale_factor / 5
        else: 
            scale = self.unit_size / max_size * scale_factor / 5
                    
        symbol_width = max_width * scale
        symbol_height = max_height * scale    
       
        index_of_end_geometry = 0
        for x in range( 0, len(geometry), 3 ):
            if geometry[x] == "0":
                index_of_end_geometry =  x
                break
            
        for x in range( 0, len( geometry ), 3 ):                    
            if geometry[x] == "1":
                start_point_x = round( float( geometry[x + 1] ) * scale - symbol_width / 2, 0 ) / 100.0
                start_point_y = round( float( geometry[x + 2] ) * scale - symbol_height / 2 , 0 ) / 100.0
                if x == 0:
                    if "SP" in skey:
                        new_geometry.append( "SpindlePoint: x0=" + str( start_point_x ) + " y0=" + str( start_point_y ) )
                    else:
                        new_geometry.append( "ArrivePoint: x0=" + str( start_point_x ) + " y0=" + str( start_point_y ) )

                elif x == ( len(geometry) - 3 ) or x == ( index_of_end_geometry - 3 ):
                    if "SP" not in skey:
                        new_geometry.append( "LeavePoint: x0=" + str( start_point_x ) + " y0=" + str( start_point_y ) )
          
            elif geometry[x] == "2":
                end_point_x = round( float( geometry[x + 1] ) * scale - symbol_width / 2 , 0 ) / 100.0
                end_point_y = round( float( geometry[x + 2] ) * scale - symbol_height / 2, 0 ) / 100.0
                new_geometry.append( "Line: x1=" + str( start_point_x ) + " y1=" + str( start_point_y ) + " x2=" + str( end_point_x ) + " y2=" + str( end_point_y ) )
                start_point_x = end_point_x
                start_point_y = end_point_y
                
            elif geometry[x] == "3":
                end_point_x = round( float( geometry[x + 1] ) * scale - symbol_width / 2, 0 ) / 100.0
                end_point_y = round( float( geometry[x + 2] ) * scale - symbol_height / 2 , 0 ) / 100.0
                new_geometry.append( "TeePoint: x0=" + str( end_point_x ) + " y0=" + str( end_point_y ) )
                start_point_x = end_point_x
                start_point_y = end_point_y
            
            elif geometry[x] == "6": 
                end_point_x = round( float( geometry[x + 1] ) * scale - symbol_width / 2, 0 ) / 100.0 
                end_point_y = round( float( geometry[x + 2] ) * scale - symbol_height / 2, 0 ) / 100.0
                new_geometry.append( "SpindlePoint: x0=" + str( end_point_x ) + " y0=" + str( end_point_y ) )
                start_point_x = end_point_x
                start_point_y = end_point_y
        
        #unique_elements = list( pd.unique( new_geometry ) )
        #return unique_elements
        return new_geometry
        
    def callLoadSkeyTree( self ):
        
        self.callLoadSkeyGroups()
        
        self.treeSkeys.clear()

        self.treeRoot = QTreeWidgetItem( self.treeSkeys )
        self.treeRoot.setText( 0, QT_TRANSLATE_NOOP( "Paragon", "Components" ) )
        self.treeRoot.setExpanded( True )
        
        self.cbSkeyGroup.clear()
        for group in self.groups:
            self.cbSkeyGroup.addItem( group )
          
        self.cbSkeyGroup.model().sort(0)
        self.cbSkeyGroup.setCurrentText( "Unknown" )
        self.cbSkeySubgroup.setCurrentText( "Unknown" )
        
        for skey_group in self.groups.keys():
            group_level = QTreeWidgetItem( self.treeRoot )
            group_level.setText( 0, skey_group )
            aIcon = QIcon( ":/PipeCad/Resources/" + skey_group[:4].upper().replace("CAPS","CAP") + ".png" )
            if aIcon.availableSizes() == ():
                aIcon = QIcon( ":/PipeCad/Resources/MISC.png" )
            group_level.setIcon(0, aIcon )
            
            for skey_subgroup in self.groups[ skey_group ].keys():
                subgroup_level = QTreeWidgetItem( group_level )
                subgroup_level.setText( 0, skey_subgroup )
                for skey in self.groups[ skey_group ][ skey_subgroup ]:
                    skey_level = QTreeWidgetItem( subgroup_level )
                    skey_level.setText( 0, skey )
                subgroup_level.sortChildren( 0, Qt.AscendingOrder )
            group_level.sortChildren( 0, Qt.AscendingOrder )
        
        
    def callSave( self ):
        if self.txtSkey.text not in self.skeys.keys():
            self.skeys[ self.txtSkey.text ] = { }
            
        self.skeys[ self.txtSkey.text ] = { "group": self.cbSkeyGroup.currentText, 
                                                "subgroup": self.cbSkeySubgroup.currentText, 
                                                "description": self.txtSkeyDesc.text, 
                                                "spindle_skey": self.cbSpindleSkey.currentText, 
                                                "scale_factor": 1.0, 
                                                "orientation": self.cbOrientation.currentIndex, 
                                                "flow_arrow": self.cbFlowArrow.currentIndex, 
                                                "dimensioned": self.cbDimensioned.currentIndex, 
                                                "geometry": []  }
        for item in self.scene.symbol_drawlist:
            if type( item ) == ArrivePoint:
                arrive_point_x0 = ( item.x() - self.scene.origin_x ) / 100.0
                arrive_point_y0 = - ( item.y() - self.scene.origin_y ) / 100.0   
                print( item.x(), item.y(), arrive_point_x0, arrive_point_y0 )
                #self.skeys[ self.txtSkey.text ]["geometry"].append( "ArrivePoint: x0=" + str( arrive_point_x0 ) + " y0=" + str( arrive_point_y0 ) )
                
            elif type( item ) == LeavePoint:
                leave_point_x0 = ( item.x() - self.scene.origin_x ) / 100.0
                leave_point_y0 = - ( item.y() - self.scene.origin_y ) / 100.0       
                #self.skeys[ self.txtSkey.text ]["geometry"].append( "LeavePoint: x0=" + str( leave_point_x0 ) + " y0=" + str( leave_point_y0 ) )
                
            elif type( item ) == TeePoint:
                tee_point_x0 = ( item.x() - self.scene.origin_x ) / 100.0
                tee_point_y0 = - ( item.y() - self.scene.origin_y ) / 100.0      
                #self.skeys[ self.txtSkey.text ]["geometry"].append( "TeePoint: x0=" + str( tee_point_x0 ) + " y0=" + str( tee_point_y0 ) )
                
            elif type( item ) == SpindlePoint:
                spindle_point_x0 = ( item.x() - self.scene.origin_x ) / 100.0
                spindle_point_y0 = - ( item.y() - self.scene.origin_y ) / 100.0        
                #self.skeys[ self.txtSkey.text ]["geometry"].append( "SpindlePoint: x0=" + str( spindle_point_x0 ) + " y0=" + str( spindle_point_y0 ) )
                
            elif type( item ) == QGraphicsLineItem:
                line_x1 = ( item.line().p1().x() - self.scene.origin_x ) / 100.0
                line_y1 = - ( self.scene.origin_y - item.line().p1().y() ) / 100.0 
                line_x2 = ( item.line().p2().x() - self.scene.origin_x ) / 100.0
                line_y2 = - ( self.scene.origin_y - item.line().p2().y() ) / 100.0 
                #self.skeys[ self.txtSkey.text ]["geometry"].append( "Line: x1=" + str( line_x1 ) + " y1=" + str( line_y1 ) + " x2=" + str( line_x2 ) + " y2=" + str( line_y2 ) )
                
            elif type( item ) == QGraphicsRectItem:
                rect_x = self.scene.convert_to_relative_position( QPointF( item.rect().x(), item.rect().y() ) ).x()
                rect_y = self.scene.convert_to_relative_position( QPointF( item.rect().x(), item.rect().y() ) ).y() 
                rect_width = round ( item.rect().width() / self.scene.step_x / 20 , 2 )
                rect_height = round ( item.rect().height() / self.scene.step_x / 20 , 2 )
                #self.skeys[ self.txtSkey.text ]["geometry"].append(  "Rectangle: x0=" + str( rect_x ) + " y0=" + str( rect_y ) + " width=" + str( rect_width ) + "Height=" + str( rect_height ) )
                
            elif type( item ) == QGraphicsPolygonItem:
                polygon_geometry = ""
                index = 1
                for point in item.polygon().toList():
                    point_x = self.scene.convert_to_relative_position( point ).x()
                    point_y = self.scene.convert_to_relative_position( point ).y()
                    polygon_geometry = polygon_geometry + " x" + str( index ) + "=" + str( point_x ) + " y" + str( index ) + "=" + str( point_y )  
                    index = index + 1
                #self.skeys[ self.txtSkey.text ]["geometry"].append(  "Polyline: " + polygon_geometry )
        
        self.callSaveToJson()    
        self.callLoadSkeyTree()        

    def callSaveToJson( self ):        
        json_object = json.dumps( self.skeys, indent = 4 )
        with open( os.getenv('PIPECAD_SETTINGS_PATH').replace( "\\\\","\\" ) + "\\iso\\IsoSymbolsLibrary.json", "w" ) as outfile:
            outfile.write( json_object )
            
    def callLoadFromJson( self ):        
        with open( self.symbol_file_json ) as json_file:
            self.skeys = json.load( json_file )
    
    def callLoadSkeyGroups( self ):
        groups = {}
        
        for skey in self.skeys.keys():
            skey_group = self.skeys[ skey ][ "group" ]
            skey_subgroup = self.skeys[ skey ][ "subgroup" ]
            if skey_group not in groups.keys():
                groups[ skey_group ] = {}
                groups[ skey_group ][ skey_subgroup ] = []
                groups[ skey_group ][ skey_subgroup ].append( skey ) 
            else:
                if skey_subgroup not in groups[ skey_group ].keys():
                    groups[ skey_group ][ skey_subgroup ] = []
                    groups[ skey_group ][ skey_subgroup ].append( skey ) 
                else:
                    if skey not in groups[ skey_group ][ skey_subgroup ]:
                        groups[ skey_group ][ skey_subgroup ].append( skey ) 
        
        for key in sorted( groups ):
            self.groups[ key ] = groups[ key ]
        
    def callSelectFileUsingExplorer( self, extension ):
        sFilePath = QFileDialog.getOpenFileName( self, QT_TRANSLATE_NOOP( "Paragon", "Select File" ), "C:\\", "Symbols file (*." + extension +")" )
        if sFilePath != "":
            return sFilePath.replace("/","\\")
    
    def callImportSkeyFromASCII( self ):
        symbol_file_path = self.callSelectFileUsingExplorer( "skey" )
        if symbol_file_path == None:
            return 
        symbol_file = open( symbol_file_path , 'r' )
        contents = symbol_file.readlines()
        skip_line = False
        new_skey = ""
        base_skey = ""
        geometry = []
        groups = {}

        max_value = 0
                
        i = -1
        for line_index in range( len(contents) ):
            row = contents[line_index]              
            
            if row[:1] == "!":
                skip_line = True
                continue
            
            record_type = row[:4].strip()
            
            if record_type == "501":
                if  new_skey != "" or  base_skey != "":
                    if new_skey != "": 
                        self.skeys[ new_skey ]["geometry"] = self.callConvertGraphics( new_skey, scale_factor, geometry )
                          
                    elif new_skey == "" and base_skey != "": 
                        self.skeys[ base_skey ]["geometry"] = self.callConvertGraphics( base_skey, scale_factor, geometry )

                geometry.clear()
                
                skip_line = False
                description = ""
                skey_group = "Unknown"
                skey_subgroup = "Unknown"
                
                new_skey = row[5:10].strip()
                base_skey = row[11:15].strip()
                
                spindle_skey = row[16:20].strip()
                scale_factor = float( row[21:29].strip() ) / 100          
                orientation = int( row[30:37].strip() )
                flow_arrow = int( row[38:45].strip() )  
                dimensioned = int( row[46:53].strip() )                
            
                if new_skey == "": 
                    if base_skey in self.skeys_desc.keys():
                        skey_group = self.skeys_desc[base_skey][0]
                        skey_subgroup = self.skeys_desc[base_skey][1]                            
                        if skey_group not in groups.keys():
                            groups[ skey_group ] = {}
                            groups[ skey_group ][ skey_subgroup ] = []
                            groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                        else:
                            if skey_subgroup not in groups[ skey_group].keys():
                                groups[ skey_group ][ skey_subgroup ] = []
                                groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                            else:
                                if base_skey not in groups[ skey_group ][ skey_subgroup ]:
                                    groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                    else:
                        if skey_group not in groups.keys():
                            groups[ skey_group ] = {}
                            groups[ skey_group ][ skey_subgroup ] = []
                            groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                        else:
                            if skey_subgroup not in groups[ skey_group].keys():
                                groups[ skey_group ][ skey_subgroup ] = []
                                groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                            else:
                                if base_skey not in groups[ skey_group ][ skey_subgroup ]:
                                    groups[ skey_group ][ skey_subgroup ].append( base_skey )                             
                    self.skeys[ base_skey ] = { "group":skey_group, "subgroup":skey_subgroup, "description": description, "spindle_skey": spindle_skey, "scale_factor": scale_factor, "orientation": orientation, "flow_arrow": flow_arrow, "dimensioned": dimensioned, "geometry": geometry  }
                    
                else:
                    if skey_group not in groups.keys():
                        groups[ skey_group ] = {}
                        groups[ skey_group ][ skey_subgroup ] = []
                        groups[ skey_group ][ skey_subgroup ].append( new_skey ) 
                    else:
                        if skey_subgroup not in groups[ skey_group].keys():
                            groups[ skey_group ][ skey_subgroup ] = []
                            groups[ skey_group ][ skey_subgroup ].append( new_skey ) 
                        else:
                            if new_skey not in groups[ skey_group ][ skey_subgroup ]:
                                groups[ skey_group ][ skey_subgroup ].append( new_skey ) 
                            
                    self.skeys[ new_skey ] = { "group":skey_group, "subgroup":skey_subgroup, "description": description, "spindle_skey": spindle_skey, "scale_factor": scale_factor, "orientation": orientation, "flow_arrow": flow_arrow, "dimensioned": dimensioned, "geometry": geometry  }

            elif record_type == "502":  
                if skip_line == True:
                    continue
                    
                pen_action_1 = row[5:14].strip()
                pos_x_1 = float( row[15:22].strip() ) 
                pos_y_1 = float( row[23:30].strip() )
                
                pen_action_2 = row[31:38].strip()
                pos_x_2 = float( row[39:46].strip() )
                pos_y_2 = float( row[47:54].strip() )
                
                pen_action_3 = row[55:63].strip()
                pos_x_3 = float( row[64:70].strip() )
                pos_y_3 = float( row[71:78].strip() )
                
                pen_action_4 = row[79:86].strip()
                pos_x_4 = float( row[87:94].strip() )
                pos_y_4 = float( row[95:103].strip() )

                geometry.append( pen_action_1 )
                geometry.append( pos_x_1 )
                geometry.append( pos_y_1 )
                geometry.append( pen_action_2 )
                geometry.append( pos_x_2 )
                geometry.append( pos_y_2 )
                geometry.append( pen_action_3 )
                geometry.append( pos_x_3 )
                geometry.append( pos_y_3 )
                geometry.append( pen_action_4 )
                geometry.append( pos_x_4 )
                geometry.append( pos_y_4 )
                
                if line_index == len(contents) - 1:
                    if new_skey != "": 
                        self.skeys[ new_skey ]["geometry"] = self.callConvertGraphics( new_skey, scale_factor, geometry )
                    elif new_skey == "" and base_skey != "": 
                        self.skeys[ base_skey ]["geometry"] = self.callConvertGraphics( base_skey, scale_factor, geometry )
                    geometry.clear()
     
        for key in sorted( groups ):
            self.groups[ key ] = groups[ key ]
        
        self.callSaveToJson()
        self.callLoadSkeyTree()   
        
    def callImportSkeyFromIDF( self ):
        symbol_file_path = self.callSelectFileUsingExplorer( "idf" )
        if symbol_file_path == None:
            return 
        symbol_file = open( symbol_file_path , 'r' )
        contents = symbol_file.readlines()
        skip_line = False
        new_skey = ""
        base_skey = ""
        geometry = []
        groups = {}

        max_value = 0
                
        i = -1
        for line_index in range( len(contents) ):
            row = contents[line_index]              
            
            if row[:1] == "!":
                skip_line = True
                continue
            
            record_type = row[:5].strip()
            
            if record_type == "501":
                if  new_skey != "" or  base_skey != "":
                    if new_skey != "": 
                        self.skeys[ new_skey ]["geometry"] = self.callConvertGraphics( new_skey, scale_factor, geometry )
                          
                    elif new_skey == "" and base_skey != "": 
                        self.skeys[ base_skey ]["geometry"] = self.callConvertGraphics( base_skey, scale_factor, geometry )
                if new_skey == "FEFL":
                    print( geometry, self.skeys[ new_skey ]["geometry"])
                geometry.clear()
                
                skip_line = False
                description = ""
                skey_group = "Unknown"
                skey_subgroup = "Unknown"
                new_skey = row[5:21].strip().split(",")[0]
                base_skey = row[5:21].strip().split(",")[1]
                spindle_skey = row[5:21].strip().split(",")[2]
                scale_factor = float( row[22:29].strip() ) / 100          
                orientation = int( row[30:37].strip() )
                flow_arrow = int( row[38:45].strip() )  
                dimensioned = int( row[46:53].strip() )                
   
                
                if new_skey == "": 
                    if base_skey in self.skeys_desc.keys():
                        skey_group = self.skeys_desc[base_skey][0]
                        skey_subgroup = self.skeys_desc[base_skey][1]
                        if skey_group not in groups.keys():
                            groups[ skey_group ] = {}
                            groups[ skey_group ][ skey_subgroup ] = []
                            groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                        else:
                            if skey_subgroup not in groups[ skey_group].keys():
                                groups[ skey_group ][ skey_subgroup ] = []
                                groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                            else:
                                if base_skey not in groups[ skey_group ][ skey_subgroup ]:
                                    groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                    else:
                        skey_group = "Unknown"
                        skey_subgroup = "Unknown"
                        if skey_group not in groups.keys():
                            groups[ skey_group ] = {}
                            groups[ skey_group ][ skey_subgroup ] = []
                            groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                        else:
                            if skey_subgroup not in groups[ skey_group].keys():
                                groups[ skey_group ][ skey_subgroup ] = []
                                groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                            else:
                                if base_skey not in groups[ skey_group ][ skey_subgroup ]:
                                    groups[ skey_group ][ skey_subgroup ].append( base_skey ) 
                                
                    self.skeys[ base_skey ] = { "group":skey_group, "subgroup":skey_subgroup, "description": description, "spindle_skey": spindle_skey, "scale_factor": scale_factor, "orientation": orientation, "flow_arrow": flow_arrow, "dimensioned": dimensioned, "geometry": geometry  }
                else:
                    if skey_group not in groups.keys():
                        groups[ skey_group ] = {}
                        groups[ skey_group ][ skey_subgroup ] = []
                        groups[ skey_group ][ skey_subgroup ].append( new_skey ) 
                    else:
                        if skey_subgroup not in groups[ skey_group].keys():
                            groups[ skey_group ][ skey_subgroup ] = []
                            groups[ skey_group ][ skey_subgroup ].append( new_skey ) 
                        else:
                            if new_skey not in groups[ skey_group ][ skey_subgroup ]:
                                groups[ skey_group ][ skey_subgroup ].append( new_skey ) 
                            
                    self.skeys[ new_skey ] = { "group":skey_group, "subgroup":skey_subgroup, "description": description, "spindle_skey": spindle_skey, "scale_factor": scale_factor, "orientation": orientation, "flow_arrow": flow_arrow, "dimensioned": dimensioned, "geometry": geometry  }
                    
            elif record_type == "502":  
                if skip_line == True:
                    continue
                    
                pen_action_1 = row[5:14].strip()
                pos_x_1 = float( row[15:22].strip() ) 
                pos_y_1 = float( row[23:30].strip() )
                
                pen_action_2 = row[31:38].strip()
                pos_x_2 = float( row[39:46].strip() )
                pos_y_2 = float( row[47:54].strip() )
                
                pen_action_3 = row[55:63].strip()
                pos_x_3 = float( row[64:70].strip() )
                pos_y_3 = float( row[71:78].strip() )
                
                pen_action_4 = row[79:86].strip()
                pos_x_4 = float( row[87:94].strip() )
                pos_y_4 = float( row[95:103].strip() )

                geometry.append( pen_action_1 )
                geometry.append( pos_x_1 )
                geometry.append( pos_y_1 )
                geometry.append( pen_action_2 )
                geometry.append( pos_x_2 )
                geometry.append( pos_y_2 )
                geometry.append( pen_action_3 )
                geometry.append( pos_x_3 )
                geometry.append( pos_y_3 )
                geometry.append( pen_action_4 )
                geometry.append( pos_x_4 )
                geometry.append( pos_y_4 )
                
                if line_index == len(contents) - 1:
                    if new_skey != "": 
                        self.skeys[ new_skey ]["geometry"] = self.callConvertGraphics( new_skey, scale_factor, geometry )
                    elif new_skey == "" and base_skey != "": 
                        self.skeys[ base_skey ]["geometry"] = self.callConvertGraphics( base_skey, scale_factor, geometry )
                    geometry.clear()
            else:
                if  new_skey != "" or base_skey != "":
                    if new_skey != "" and self.skeys[ new_skey ]["geometry"] != []: 
                        self.skeys[ new_skey ]["geometry"] = self.callConvertGraphics( new_skey, scale_factor, geometry )
                          
                    elif new_skey == "" and base_skey != "" and self.skeys[ new_skey ]["geometry"] != []: 
                        self.skeys[ base_skey ]["geometry"] = self.callConvertGraphics( base_skey, scale_factor, geometry )

                    geometry.clear()
                    new_skey = "" 
                    base_skey = ""
                else:
                    pass
                
        for key in sorted( groups ):
            self.groups[ key ] = groups[ key ]
            
        self.callLoadSkeyTree()
    
# Singleton Instance.
aSkeyEditorDialog = SkeyEditorDialog(PipeCad)

def show():
    aSkeyEditorDialog.show()
    
        
