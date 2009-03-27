# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class TableMill:


    def __init__(self, configurations):
        self.configurations = configurations
        return


    def onTable(self, table):
        configurations = self.configurations
        home = configurations['home']
        
        csscode = []
        csss = [
            'tabulator/datePicker.css',
            'tabulator/tabulator.css',
            'tabulator/tabulator-color.css',
            ]
        for css in csss:
            csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/%s" />' % (
                home,css) )

        htmlcode = []
        id = _id(table)
        htmlcode.append( '<div id="%s">' % id )
        htmlcode.append( '</div>' )

        codes = csscode + htmlcode
        return codes


class JSMill:

    def onTable(self, table):
        id = _id(table)
        table = towidgetdescription(table)
        return self._onTable(table, id)
    
    
    def _onTable(self, table, id):
        includes = [
            'jquery/jquery.js',
            'jquery/date.js',
            'jquery/jquery.datePicker.js',
            'jquery/tabulator.js',
            'jquery/elementFactory.js',
            'jquery/tableFactory.js',
            ]
        self.include(scripts=includes)

        self.writemain( 'Date.firstDayOfWeek = 7;')
        self.writemain( 'Date.format = "mm/dd/yyyy";' )
        
        self.writemain( 'thetablediv = $("#%s");' % id )
        descriptors = table.column_descriptors
        self.writemain(
            'descriptors={%s};' %
            ',\n'.join( [jscode_descriptor( d ) for d in descriptors] )
            )
        self.writemain( 'thetable = tableFactory.createTable( thetablediv, descriptors);' )

        # data
        self.writemain(
            'rows = [\n%s\n];' %
            ',\n\n\t'.join(
                ["{'id': '%s', 'data': [%s]}" % (
                    i, ',\n\t\t'.join( [
            format(v, descriptor) for v, descriptor in zip(row, table.column_descriptors) ] ) )
                 for i, row in enumerate(table.rows)
                 ])
            )

        self.writemain('thetable.table_appendrows_dataonly(rows);')

        self.writemain( 'thetable.addClass( "tabulated" );' );

        if table.editable:
            self.writemain( '''
            thetable.find( 'tbody' ).find( "td[datatype=text]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')
        
            self.writemain( '''
            thetable.find( 'tbody' ).find( "td[datatype=money]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')

            self.writemain( '''
            thetable.find( 'tbody' ).find( "td[datatype=single_choice]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')

            self.writemain( '''
            thetable.find( 'tbody' ).find( "td[datatype=date]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')


        return



# helpers

def _id(table):
    # html id for renderred table
    return id(table)


def format(value, descriptor):
    handler = '_format_%s' % descriptor.datatype
    handler = eval(handler)
    return handler(value)

#def _format_link(value):
#    # value is a JnlpFile object--rename to remind
#    name,link = value
#    return repr('<a href="'+link+'">'+name+'</a>')

def _format_text(value):
    value = str(value)
    v = value.replace('\n', '<BR>')
    return repr(v)

def _format_date(value): 
    return repr(str(value))

def _format_single_choice_in_one_column(value): 
    items_str = ', '.join([repr(str(k))+" : "+repr(str(v)) for k,v in value.iteritems()])
    return '{' + items_str + '}'



def jscode_descriptor( descriptor ):
    d = { 'text': descriptor.label, 'datatype': descriptor.datatype }
    d.update(descriptor.options)
    
    return "%r : { %s }" % (descriptor.id, ','.join(
        [ '%s: %r' % (k,v) for k,v in d.iteritems() ] ) )



def towidgetdescription(table):
    # table is an instance of vnf.content.table.Table
    # return: an instance of vnf.weaver.table.Table

    # column descriptors
    from table.Column import Column
    coldescs = []
    for col in table.view.columns:
        id = col.id
        label = col.label
        measure = table.model.getMeasure(col.measure)
        datatype = measure.type
        options = col.options
        coldesc = Column(id=id, label=label, datatype=datatype, **options)
        coldescs.append(coldesc)
        continue

    # data
    rows = []
    for d in table.data:
        row = [getattr(d, col.measure) for col in table.view.columns]
        rows.append(row)
        continue
    
    from table.Table import Table
    return Table(coldescs, rows, editable = table.view.editable)

import os


def test():
    from vnf.content.table.Table import example
    table = example()
    configurations = {
        'home': '**home**',
        'cgihome': '**cgihome**',
        }
    renderer = TableMill(configurations)
    print '\n'.join(renderer.render(table))
    return

def main():
    test()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
