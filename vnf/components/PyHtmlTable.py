#!/usr/local/bin/python

"""
-----------------------------------------
                Class PyHtmlTable

What:

     Html Table generation on the fly.

Why:
     Couldn't find an equivalent to Table.pm or Table.php

Features:

  Allows setting of individual row and cell attributes via arbitrary
  dictionaries

  Allows spanning of rows and columns

  Autogrows table if cells set outside initial
  Range.

  Allows dynamic insertion of new rows and columns anywhere in the table

  Allows bulk population of table data via arrays to arbitrary locations
  in the table.

  Provides default cell attributes for tablewide uniformity
  and the ability to override these on a cell by cell basis.

  NOTE: Row indexes start at 0 like God and Kernighan demand!

Influenced heavily by Table.pm and Table.php

Example

    print "<b> 2 by 2 table </b> "
    
    t  = PyHtmlTable(2,2, {'width':'400','border':2,'bgcolor':'white'})

    t.setCellcontents(0,0,"T1 Cell 00")
    t.setCellcontents(0,1,"T1 Cell 01")
    t.setc(1,0,"T1 Cell 01")            # New shorthand: setc == setCellcontents
    t.setc(1,1,"T1 Cell 11")            # Most of the main functions now have horthand equivalents

    t.setCellattrs(0,0,{'bgcolor':'red','width':100})
    t.setca(1,1,{'bgcolor':'red'})      # New shorthand: setca == setCellattrs
    t.display()

    t.setCellcontents(2,0,"T1 Cell 20")  # Grow outside initial bounds
    t.setCellcontents(2,1,"T1 Cell 21")
    t.display()

    print "<p><b> adding row </b>"

    t.add_row(1)   #Add a row after row index 1
    t.display()

    print "<p><b> adding col </b>"

    t.add_col(1)   #Add a col after col index 1
    t.display()

    print "<HR><b> AFTER  row and col SPANNING </b>"
    t.setCellRowSpan(1,0,2) # Span cell at index row 1,col 0, make 2 high
    t.setCellColSpan(1,1,2) # colSpan cell at index row 1, col 1, make 2 wide

    t.display()

    print "<HR><b> Embed in new table </b>"

    htmlstr = t.return_html()
    nt = PyHtmlTable(1,4, {'width':'800','border':2,'bgcolor':'green'})

    nt.setCellcontents(0,0,"Cell TH....text left")
    nt.setCellcontents(0,1,"Text right")
    nt.setCellcontents(0,2,htmlstr)

    nt.setCellattrs(0,0,{'bgcolor':'blue','width':200,'align':'left'})

    nt.setCellattrs(0,1,{'width':200,'align':'right'})

    nt.setCelltype(0,0,"TH")

    nt.display()


    Current-Version:         $Revision: 1.13 $
    Last update:             $Date: 2003/07/24 14:21:21 $

    Home-Page:               http://pasko.net/PyHtmlTable
    Primary-Site:            http://pasko.net/PyHtmlTable
    Software-requirements:   twodarr.py

    Written and debugged under Python 2.2.2 by Joe Pasko

"""



import string,re
import copy
import twodarr
import sys

class PyHtmlTable:

    def __init__( self, rows, cols, tattr=None ):

        self.htcells = twodarr.twodarr( rows, cols, '&nbsp;' )

        self.tabattr     = ""          # Holds border=FOO, color=bar pairs
        self.cellattr    = {}          # <TD . $attr  (row,col) tuple
        self.endcellattr = {}          # $attr . </TD>
        self.colattr     = {}          
        self.rowattr     = {}          # <TR = $attr indexed by row

        self.celltype       = {}       # TH, TD indexed by (row,col) tuple

        self.celldefattrs   = ""

        self.overwriteattrs = 0        # On data insertion, should we append or
                                       # overwrite cell attributes, defaults to
                                       # append

        self.maxRow   = self.htcells.get_num_rows()
        self.maxCol   = self.htcells.get_num_cols()

        self.defctype = "TD"

        self.spantext = '<!-- spanned cell -->'

        if tattr !=None:                 # Handle table attrs if passed in
            self.setTableattrs( tattr )

#-----------------------------------------
    def setCellDefattrs( self, indict ):

        """Sets default attributes for cells in table
           Used if cell does not have specific atributes """

        for key in indict.keys():
            val       = indict[key]
            newattr   = """%s="%s" """ % ( key, val )

            self.celldefattrs = self.celldefattrs + newattr
#-----------------------------------------
    def getCellDefattrs( self ):
        """Returns default cell attributes"""
        return self.celldefattrs

#-----------------------------------------
    def clearCellDefattrs( self ):
        """Clears default cell attributes"""
        self.celldefattrs = None

#-----------------------------------------
    def add_array_to_row( self, row, col, inarr, attrs=None ):

        """Adds list of data specified by inarr to table object
          starting at row,col

          Optionally specify attributes to set on cells being added
          by defining the attrs dictionary

          Note: Cell attribute insertion can be additive or overwriting depending
                on calls to setReplaceCellattrs() or setAppendCellattrs()

                Default is to append new attributes


          """
        
        arlen = len( inarr )


        for i in range( arlen ):
            self.setCellcontents( row, col+i, inarr[i], attrs )

#-----------------------------------------
    def add_array_to_col( self, row, col, inarr, attrs=None ):

        """Adds list of data specified by inarr to table object
          starting at row,col

          Optionally specify attributes to set on cells being added
          by defining the attrs dictionary

          
          Note: Cell attribute insertion can be additive or overwriting depending
                on calls to setReplaceCellattrs() or setAppendCellattrs()

                Default is to append new attributes

                """

        arlen = len( inarr )

        for i in range( arlen ):
            self.setCellcontents( row+i, col, inarr[i], attrs )
        

#-----------------------------------------
    def setCellColSpan( self, row, col, numcells ):
        """Sets COLSPAN starting at rowidx, colidx
           spanning numcells 
           (Remember rows,cols start at 0,0)"""
           

        for f in range( col + 1 , col + numcells ):
            self.setCellcontents( row, f, self.spantext )
        
        self.setCellattrs( row, col,{'COLSPAN':numcells} )


#-----------------------------------------
    def setCellRowSpan( self, row, col, numcells ):
        """Sets ROWSPAN starting at rowidx, colidx
           spanning numcells 
           (Remember rows,cols start at 0,0)"""
        for f in range( row + 1 , row + numcells ):
            self.setCellcontents( f, col, self.spantext )

        self.setCellattrs( row, col,{'ROWSPAN':numcells} )


#-----------------------------------------
    def __dumpattrs( self, indict ):

        print "\n\n----dumping generic attrs ----"        
        print indict
        print "\n\n "

#-----------------------------------------
    def __start_row( self, row ):

        ratter = self.getRowattrs( row )


        if ratter:
            trow = "<TR " + str(ratter) + " >"
        else:
            trow = "<TR>"

        return trow

#-----------------------------------------
    def __end_row( self ):
        return "</TR>"

#-----------------------------------------
    def __end_table( self ):
        return "</TABLE>"

#-----------------------------------------
    def setColattrs( self, col, indict ):
        """Presently unused"""
        if col >= self.maxCol:
#            print "INdexs out of range"
            return None
        
        for key in indict.keys():
            val = indict[key]
            if( self.colattr.has_key( col ) ):
                pval = self.colattr[ (col) ]
                self.colattr[ col ]  =  """%s, %s="%s" """ %  ( pval, key, val )
            else:
                 self.colattr[ col ] =  """%s="%s" """ % ( key, val )


#-----------------------------------------
    def setRowattrs( self, row, indict ):
        """Sets attributes for give rowidx

           indict is a dictionary of key=val pairs
           {'bgcolor':'black'} translates to <TR BGCOLOR="BLACK">

           """

        if row >= self.maxRow:
#            print "INdexs ROW out of range"
            return None
        
        for key in indict.keys():

            val = indict[key]

            if( self.rowattr.has_key( row ) ):
                pval = self.rowattr[ (row) ]
                self.rowattr[ row ] =  """%s, %s="%s" """ %  ( pval, key, val )
            else:
                 self.rowattr[ row ] ="""%s="%s" """ % ( key, val )


#-----------------------------------------
    def getRowattrs( self, row ):

        """ Returns attribute string for given rowidx which
            was set by setRowattrs"""

        if not self.rowattr.has_key( row ):
            return None
        
        return self.rowattr[ row ]

#-----------------------------------------
    def getColattrs( self, col ):

        """Presently unused"""

        if not self.colattr.has_key( col  ):
            return None

        return self.colattr[ col ]

#-----------------------------------------
    def getCellattrs( self, row, col ):

        """ Returns attributes set for specific cell at rowidx colidx """

        if not self.cellattr.has_key( (row, col) ):
            return None

        return self.cellattr[ (row,col) ]

#-----------------------------------------
    def __getendCellattrs( self, row, col ):
        """Presently unused"""

        if not self.endcellattr.has_key( (row,col) ):
            return None

        return self.endcellattr[ (row,col) ]

#-----------------------------------------
    def __setendCellattrs( self, row, col, indict ):

        """Presently unused"""

        if row >= self.maxRow or col >= self.maxCol:
#            print "INdexs out of range"
            return None
        
        for key in indict.keys():
            val = indict[key]
            if( self.endcellattr.has_key( (row,col) ) ):
                pval = self.endcellattr[ (row,col) ]
                self.endcellattr[ (row,col) ] =  """%s, %s="%s" """ %  ( pval, key, val )
            else:
                 self.endcellattr[ (row,col) ] ="""%s="%s" """ % ( key, val )


#-----------------------------------------
    def setCellattrs( self, row, col, indict ):

        """ Sets cell attributes for cell at rowidx, colidx

            indict is a dictionary of key=val pairs

           {'bgcolor':'black', 'width':200} yields

           <TD BGCOLOR="BLACK" width="200" >
           on output
        """

        if row >= self.maxRow or col >= self.maxCol:
#            print "INdexs out of range"
            return None

        if self.overwriteattrs == 1:
            self.clearCellattrs( row, col )

        for key in indict.keys():

            val = indict[key]

            if( self.cellattr.has_key( (row,col) ) ):

                pval = self.cellattr[ (row,col) ]
                self.cellattr[ (row,col) ] =  """%s, %s="%s" """ % ( pval, key, val )
                
            else:
                 self.cellattr[ (row,col) ] ="""%s="%s" """ % ( key, val )

#-----------------------------------------
    def setTableattrs( self, indict ):

        """ Sets table attributes in <TABLE directive

            indict is a dictionary of key=val pairs
            {'width':'800','border':2,'bgcolor':'green'} yields

            <TABLE WIDTH="800" BORDER="2" BGCOLOR="GREEN">
            """

        for key in indict.keys():
            val = indict[key]
            tpair = """  %s="%s" """ % (key,val)
            self.tabattr = self.tabattr + tpair
            
#-----------------------------------------
    def setCelltype( self, row, col, ctype="TD" ):

        """ Celltypes can be TD or TH """

        if row >= self.maxRow or col >= self.maxCol:
#            print "INdexs out of range"
            return None
        
        self.celltype[ (row,col) ] = ctype

#-----------------------------------------
    def getCelltype( self, row, col ):

        """ Returns Celltypes which is TD or TH """

        if row >= self.maxRow or col >= self.maxCol:
#            print "INdexs out of range"
            return None
        
        if self.celltype.has_key( (row,col) ):
            return self.celltype[ (row,col) ]
        else:
            return "TD"
#-----------------------------------------
    def setReplaceCellattrs( self ):

        """After calling this function calls to setCellattrs() will
        append attribute information to cells

        If the cell had attributes width="400", after calling this
        function calls to setCellattrs( x, y, {'bgcolor':'black'})
        yields attributes for cell x,y of:

                bgcolor="black"

        """
        self.overwriteattrs = 1

#-----------------------------------------
    def setAppendCellattrs( self ):

        """After calling this function calls to setCellattrs() will
        append attribute information to cells

        If the cell had attributes width="400", after calling this
        function calls to setCellattrs( x, y, {'bgcolor':'black'})
        yields attributes for cell x,y of:

                 width="400" bgcolor="black"

        Note: This is the default behavior

        """

        self.overwriteattrs = 0

#-----------------------------------------
    def setCellcontents( self, row, col, data, attrs=None ):

        """ Puts data into cell at rowidx, colidx
            Takes optional attribute dictionary for cell"""


        # Force casting as a string
        if data != None:
            data = str( data )

        if data == None:
            data = '&nbsp;'

        if data == "":
            data = '&nbsp;'

        self.htcells.set_cell( row, col, data )

        # May have need to grow the table in the twodarray class
        # Query class to reset max row/cols if necessary

        self.maxRow = self.htcells.get_num_rows()
        self.maxCol = self.htcells.get_num_cols()

        if attrs != None:

            if self.overwriteattrs == 1:
                self.clearCellattrs( row, col )

            self.setCellattrs( row, col, attrs )


#-----------------------------------------    
    def clearCellattrs( self, row, col ):

        """ Clear cells attributes """

        if not self.cellattr.has_key( (row,col) ):
            return None

        del self.cellattr[ (row,col) ]
#-----------------------------------------    
    def clearRowattrs( self, row ):

        """ Clear row attributes """

        if not self.rowattr.has_key( row ):
            return None

        del self.rowattr[ row ]

#-----------------------------------------    
    def clearTableattrs( self ):

        """ Clear Table attributes """

        self.tabattr     = ""

#-----------------------------------------    
    def getCellcontents( self, row, col ):

        """ Get cells stored data values
            Return an &nbsp if cell is None
        """

        retstr = self.htcells.get_cell( row, col )  


        if retstr == None:
            return "&nbsp;"
        else:
            return retstr


#-----------------------------------------    
    def getmaxRow( self ):

        """ Returns index of highest row( number_of_rows -1 )"""

        return self.maxRow -1 

#-----------------------------------------
    def getmaxCol( self ):

        """ Returns index of highest col( number_of_cols -1 )"""

        return self.maxCol -1 

#-----------------------------------------
    def __start_table( self ):
        
        if self.tabattr != "":
            stag = "<TABLE %s>" % self.tabattr
            return stag
        else:
            return "<TABLE>"
        
#-----------------------------------------
    def __has_only_rowcolsp_attrs( self, attrstr ):

        if attrstr == None or attrstr == "":
            return 0

        colpat      = re.compile( 'COLspan="\w+', re.IGNORECASE )
        rowpat      = re.compile( 'ROWspan="\w+', re.IGNORECASE )
        multieqpat  = re.compile( '.*=.*='                   )

        if not re.match( colpat, attrstr ) and  not re.match( rowpat, attrstr ):
            return 0    # we didn't have colspan or rowspan at all

        if not re.match( multieqpat, attrstr ):
            return 1

               # We've got two equals, now check to see if any left
               # After we nuke colspan and rowspan

        attrstr  = re.sub(colpat,'', attrstr)
            
        attrstr  = re.sub(rowpat,'', attrstr)

        if re.match( '.*=.*', attrstr ): #We have some other attribute left over
            return 0
        
        return 1


        




#-----------------------------------------
    def __resCell( self, row, col ):

        data   = self.getCellcontents( row, col )

        # Must be a spanned cell, don't print anything
        if data == self.spantext:
            return None


        ctype      = self.getCelltype ( row, col )

        cattr      = self.getCellattrs( row, col ) 

        ceattr     = self.__getendCellattrs( row, col )

        cdefattr   = self.getCellDefattrs() 

        closetag   = "</%s>" % ctype

        if cattr != None:

            # If we only have a single rowspan/colspan attribute, merge it with
            # the default cell attributes IF NO OTHER ATTRIBUTES EXIST FOR THAT CELL

            if cdefattr != "" and self.__has_only_rowcolsp_attrs(  cattr  ) == 1  :

                retstr = "<%s %s>" % ( ctype,  cdefattr + " " +  cattr ) 

            else: 
                retstr = "<%s %s>" % ( ctype,  cattr ) 

        elif cdefattr != "":  

            retstr = "<%s %s>" % ( ctype,  str( cdefattr ) )

        else: 

            retstr = "<%s>" % ctype

        retstr = retstr + str( data )          # Add the meat of the cell


        # Process closing tags

        if ceattr != None:
            retstr = retstr + ceattr + closetag
        else:
            retstr = retstr + closetag

        return retstr

#--------------------------------------------------------
# Run through the cells and adjust the tuple indexes down
    def __adjust_dbl_indx_dict_rows_down( self, indict, add_after_this_row ):


        for i in range( self.maxRow, add_after_this_row, -1 ):
        
            for key in indict.keys():
                row,col = int( key[0] ), int( key[1] )
                if row != i:
                    continue

                val = indict[key]

                indict[ ( row+1, col ) ] = val

                del indict[ ( row, col ) ]

#--------------------------------------------------------
    def add_row( self, row ):

        """ Adds row to table after specified rowidx.
            Adding row at rowidx -1 adds row to top of table """

        if row > self.maxRow:
            row = self.maxRow

        # Update attrs for rowattr, cellattr, then call
        # array updater, 

        if row != self.maxRow-1:   #Adding row to bottom, no need to move attrs
            self.__adjust_dict_rows_down( self.rowattr, row )

            self.__adjust_dbl_indx_dict_rows_down( self.cellattr, row )
            self.__adjust_dbl_indx_dict_rows_down( self.celltype, row )

        self.__adjust_2d_array_rows_down(      self.htcells,  row )

#--------------------------------------------------------
    def add_col( self, col ):

        """ Adds col to table after specified colidx 
            Adding col at colidx -1 adds col to left of table """

        if col > self.maxCol:
            col = self.maxCol

        # Update attrs for colattr, cellattr, then call
        # array updater, 

        if col != self.maxCol-1 :   #If Adding col to right,skip moving attrs

            self.__adjust_dict_cols_right(          self.rowattr,  col )
            self.__adjust_dbl_indx_dict_cols_right( self.cellattr, col )
            self.__adjust_dbl_indx_dict_cols_right( self.celltype, col )

        self.__adjust_2d_array_cols_right(      self.htcells,  col )
        
#--------------------------------------------------------
# Run through the cells and adjust the tuple index down
    def __adjust_dict_rows_down( self, indict, add_after_this_row ):

        if add_after_this_row == self.maxRow-1:
            return

        if add_after_this_row == -1:

            for i in range( self.maxRow, 0, -1 ):
                if indict.has_key( i-1 ):
                    val = indict[i-1]
                    indict[i] = val
                    del  indict[i-1]
            return

        for i in range( self.maxRow, add_after_this_row, -1 ):
            if indict.has_key( i-1 ):
                val = indict[i-1]
                indict[i] = val
                del  indict[i-1]

#--------------------------------------------------------
    def __adjust_dict_cols_right( self, indict, add_after_this_col ):

        if add_after_this_col == self.maxCol-1:
            return
        
        if add_after_this_col == -1:
            for i in range( self.maxCol, 0, -1 ):
                if indict.has_key( i-1 ):
                    val = indict[i-1]
                    indict[i] = val
                    del  indict[i-1]
            return

        for i in range( self.maxCol, add_after_this_col, -1 ):
            if indict.has_key( i-1 ):
                val = indict[i-1]
                indict[i] = val
                del  indict[i-1]

#--------------------------------------------------------
    def __adjust_dbl_indx_dict_cols_right( self, indict, shift_after_this_col ):
        
        for i in range( self.maxCol, shift_after_this_col, -1 ):
        
            for key in indict.keys():
                row,col = int( key[0] ), int( key[1] )
                if col != i:
                    continue

                val = indict[key]

                indict[( row, col+1 )] = val
                del indict[( row, col )]

#--------------------------------------------------------
    def __adjust_2d_array_rows_down( self, inarr, add_after_this_row ):

        self.maxRow = inarr.get_num_rows()
        self.maxCol = inarr.get_num_cols()

        deffill     = self.htcells.filltype

        #Adding to bottom, no need to move data
        if self.maxRow - 1 == add_after_this_row :

            i = self.maxRow

            for j in range( self.maxCol ):

                inarr.set_cell( i, j, deffill )

            self.maxRow   = self.htcells.get_num_rows()
            self.maxCol   = self.htcells.get_num_cols()

            return

        for i in range( self.maxRow, add_after_this_row+1, -1 ):

            for j in range( self.maxCol ):
            
                data2mv = inarr.get_cell( i-1,j )


                inarr.set_cell( i,   j, data2mv )

                inarr.set_cell( i-1, j, deffill )
               
                self.maxRow   = self.htcells.get_num_rows()
                self.maxCol   = self.htcells.get_num_cols()

#-----------------------------------------
    def __adjust_2d_array_cols_right( self, inarr, add_after_this_col ):

        self.maxRow = inarr.get_num_rows()
        self.maxCol = inarr.get_num_cols()

        deffill     = self.htcells.filltype


        # Adding cols to right edge no need for data moving

        if(  self.maxCol-1  == add_after_this_col ): 

            i = self.maxCol

            for j in range( self.maxRow ):

                inarr.set_cell( j,   i, deffill )

            self.maxRow   = self.htcells.get_num_rows()
            self.maxCol   = self.htcells.get_num_cols()

            return

        # Shift data
        for i in range( self.maxCol, add_after_this_col + 1, -1 ):
            for j in range( self.maxRow ):
            
                data2mv = inarr.get_cell( j, i-1 )
            
                inarr.set_cell( j,   i, data2mv )
                inarr.set_cell( j, i-1,  deffill )

        self.maxRow   = self.htcells.get_num_rows()
        self.maxCol   = self.htcells.get_num_cols()

#-----------------------------------------
    def display( self ):

        """ Prints html table """

        ts = self.__start_table()
        print ts

        for row in range( self.maxRow ):

            tr  = self.__start_row( row )
            trc = self.__end_row  (     )

            print tr

            for col in range( self.maxCol ):

                td = self.__resCell( row, col )

                if td:
                    print td

            print trc,"\n"

        print self.__end_table()
        sys.stdout.flush()

#-----------------------------------------------------------------------
# Probably going to take more memory than printing as it's being generated
# and stored in memory ymmv...

    def return_html( self ):

        """ Returns html table as string """

        htmltbl = []

        ts = self.__start_table()
 
        htmltbl.append( ts )

        for row in range( self.maxRow ):

            tr  = self.__start_row( row )
            trc = self.__end_row  (     )

            htmltbl.append(  tr )

            for col in range( self.maxCol ):

                td = self.__resCell( row,col )

                if td:                       #Spanned cells return None
                    htmltbl.append(  td )

            htmltbl.append(  trc +  "\n" )

        htmltbl.append( self.__end_table() + "\n\n" ) 

        return string.join( htmltbl, '' )


#**************************************************************
#             Shortcut section
#**************************************************************
    

    def addar2r(self, row, col, inarr, attrs=None ):
        """Calls add_array_to_row """
        self.add_array_to_row( row, col, inarr, attrs )

    def addar2c(self, row, col, inarr, attrs=None ):
        """Calls add_array_to_col"""
        self.add_array_to_col( row, col, inarr, attrs )

    def clearcda( self ):
        """Calls clearCellDefattrs """
        self.clearCellDefattrs()

    def getc( self, row, col ):
        """Calls getCellcontents """
        return self.getCellcontents( row, col ) 

    def getcda( self, indict ):
        """Calls  getCellDefattrs"""
        return self.getCellDefattrs()

    def getct(self, row, col ):
        """Calls  getCelltype """
        return self.getCelltype( row, col )

    def setc( self, row, col, data, attrs=None  ):
        """Calls setCellcontents"""
        self.setCellcontents( row, col, data, attrs )
    
    def setca(self, row, col, indict  ):
        """Calls setCellattrs """
        self.setCellattrs( row, col, indict )

    def setcda( self, indict ):
        """Calls setCellDefattrs """
        self.setCellDefattrs( indict )

    def setcrspan( self, row, col, numcells ):
        """Calls setCellRowSpan"""
        self.setCellRowSpan(  row, col, numcells )

    def setcspan( self, row, col, numcells ):
        """Calls setCellColSpan"""
        self.setCellColSpan( row, col, numcells )

    def setct( self, row, col, ctype="TD" ):
        """Calls setCelltype"""
        self.setCelltype( row, col, ctype )
    
    def setta( self, indict ):
        """Calls setTableattrs"""
        self.setTableattrs( indict )

#-------------------------------------------------------------
#           Example html, if run from cmd line
#-------------------------------------------------------------
def main():
    print 'Content-Type: text/html\n\n'
    print """<HTML><HEAD></HEAD><BODY bgcolor="white"> """


    print "<b> 2 by 2 table</b> "
    
    t  = PyHtmlTable(2,2, { 'width':'400', 'border':2, 'bgcolor':'white'} )

    t.setCellcontents(0,0,"T1 Cell 00")
    t.setCellcontents(0,1,"T1 Cell 01")
    t.setCellcontents(1,0,"T1 Cell 01")
    t.setCellcontents(1,1,"T1 Cell 11")

    t.setCellattrs(0,0,{'bgcolor':'red','width':100})
    t.setCellattrs(1,1,{'bgcolor':'red'})
    t.display()

    print """<b>Dynamically grow outside initial table boundaries by setting
                cells outside current boundaries </b>"""
                  
    t.setCellcontents(2,0,"T1 Cell 20")  # Grow outside initial bounds
    t.setCellcontents(2,1,"T1 Cell 21")
    t.display()

    print "<p><b> Explicitly add row after row index 1 </b>"

    t.add_row(1)   #Add a row after row index 1
    t.display()

    print "<p><b> Explicitly adding col after column index 1 </b>"

    t.add_col(1)   #Add a col after col index 1
    t.display()

    print "<HR><b> AFTER  row and col SPANNING </b>"
    t.setCellRowSpan(1,0,2) # Span cell at index row 1,col 0, make 2 high
    t.setCellColSpan(1,1,2) # colSpan cell at index row 1, col 1, make 2 wide

    t.display()

    print "<HR><b> Embed in new table </b>"

    htmlstr = t.return_html()
    nt = PyHtmlTable(1,4, {'width':'800','border':2,'bgcolor':'green'})

    nt.setCellcontents(0,0,"Cell TH....text left")
    nt.setCellcontents(0,1,"Text right")
    nt.setCellcontents(0,2,htmlstr)

    nt.setCellattrs(0,0,{'bgcolor':'blue','width':200,'align':'left'})

    nt.setCellattrs(0,1,{'width':200,'align':'right'})

    nt.setCelltype(0,0,"TH")

    nt.display()

    print "</BODY></HTML>"

if __name__ == "__main__":
    main()
