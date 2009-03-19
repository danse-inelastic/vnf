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


    # this is a temporary 
    def render(self, table):
        table = towidgetdescription(table)
        return self._render(table)
    
    
    def _render(self, table):
        configurations = self.configurations
        home = configurations['home']
        cgihome = configurations['cgihome']
        
        csscode = []
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/tabulator/datePicker.css" />' % home )
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/tabulator/tabulator.css" />' % home )
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/tabulator/tabulator-color.css" />' % home )

        htmlcode = []
        gid = id(table)
        htmlcode.append( '<div id="%s">' % gid )
        htmlcode.append( '</div>' )

        includes = []
        javascriptpath = os.path.join(home, 'javascripts')
        
        includes.append( '<SCRIPT src="%s/jquery/jquery.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/date.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/jquery.datePicker.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/tabulator.js"></SCRIPT>' % javascriptpath )

        jscode = []
        jscode.append('''
function make_form() {
  return $( '<form> </form>' );
}
''')
        jscode.append('''
function make_table_skeleton( ) {
  
  table = $( '<table border="1"></table>' );
  
  thead = $( '<thead></thead' );
  table.append(thead);
  
  headrow = $( '<tr></tr>' );
  thead.append( headrow );

  tbody = $( '<tbody></tbody>' );
  table.append( tbody );
  
  return table;
}
''')

        jscode.append('''
function add_headcell( id, text, headrow )
{
  cell = $( '<td id="' + id + '">' + text + '</td>' );
  headrow.append( cell );
  return cell;
}
''')

        jscode.append('''
function establish_headrow_from_column_descriptors( headrow, descriptors )
{
  for (var colid in descriptors) {
    descriptor = descriptors[ colid ];
    cell = add_headcell( colid, descriptor.text, headrow );

  }
}
''')

        jscode.append('''
function make_table_head( thetable, descriptors ) {

  thead = $(thetable.children( 'thead' )[0]);
  headrow = $(thead.children( 'tr' )[0]);
  
  establish_headrow_from_column_descriptors( headrow, descriptors );
  thetable.table_setcolumndescriptors( descriptors );
  for (var colid in descriptors) {
    thetable.sortable_column(colid);
  }
}
''')

        jscode.append( '''
function make_table( div, descriptors ) {
  
  // table skeleton
  thetable = make_table_skeleton();

  // add table to a form
  // form = make_form();
  // form.append( thetable );
  
  // add form to the division
  // div.append( form );
  div.append(thetable);
  
  // contents of table
  // head
  make_table_head( thetable, descriptors );
}
''');
        jscode.append( '$(document).ready(function() {')
        
        jscode.append( 'Date.firstDayOfWeek = 7;')
        jscode.append( 'Date.format = "mm/dd/yyyy";' )
        
        jscode.append( 'thetable = $("#%s");' % gid )
        descriptors = table.column_descriptors
        jscode.append(
            'descriptors={%s};' %
            ',\n'.join( [jscode_descriptor( d ) for d in descriptors] )
            )
        jscode.append( 'make_table( thetable, descriptors);' )

        jscode.append(
            'rows = [\n%s\n];' %
            ',\n\n\t'.join(
                ["{'id': '%s', 'data': [%s]}" % (
                    i, ',\n\t\t'.join( [
            format(v, descriptor) for v, descriptor in zip(row, table.column_descriptors) ] ) )
                 for i, row in enumerate(table.rows)
                 ])
            )
        #for i, row in enumerate(table.rows):
        #    jscode.append(
        #        'thetable.table_appendrow_dataonly(%d, [%s]);' %
        #        (i, ','.join( ['%r' % v for v in row] ) )
        #        )
        #    continue
        jscode.append('thetable.table_appendrows_dataonly(rows);')

        jscode.append( 'thetable.addClass( "tabulated" );' );

        if table.editable:
            jscode.append( '''
            thetable.find( 'tbody' ).find( "td[datatype=text]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')
        
            jscode.append( '''
            thetable.find( 'tbody' ).find( "td[datatype=money]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')

            jscode.append( '''
            thetable.find( 'tbody' ).find( "td[datatype=single_choice]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')

            jscode.append( '''
            thetable.find( 'tbody' ).find( "td[datatype=date]" ).dblclick( function () {
            $(this).enable_cell_editing();
            } );
            ''')

        jscode.append( '});' );
        
        codes = csscode + includes + ['<script>']  + jscode + ['</script>'] + htmlcode
        return codes



def format(value, descriptor):
    handler = '_format_%s' % descriptor.datatype
    handler = eval(handler)
    return handler(value)

def _format_link(value):
    # value is a JnlpFile object--rename to remind
    name,link = value
    return '<a href="'+link+'">'+name+'</a>'

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
