// -*- JavaScript -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                         (C) 2008 All Rights Reserved  
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


var tableFactory = {};


(function (d, $) {

  // createTable in the given division 
  // descriptors: descriptors of columns
  d.createTable = function ( div, descriptors ) {
    
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

    return thetable;
  };
  
  function make_form() {
    return $( '<form> </form>' );
  }

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

  
  function add_headcell( id, text, headrow )
  {
    cell = $( '<td id="' + id + '">' + text + '</td>' );
    headrow.append( cell );
    return cell;
  }
  
  
  function establish_headrow_from_column_descriptors( headrow, descriptors )
  {
    for (var colid in descriptors) {
      descriptor = descriptors[ colid ];
      cell = add_headcell( colid, descriptor.text, headrow );
    }
  }
  
  
  function make_table_head( thetable, descriptors ) {
    
    thead = $(thetable.children( 'thead' )[0]);
    headrow = $(thead.children( 'tr' )[0]);
    
    establish_headrow_from_column_descriptors( headrow, descriptors );
    thetable.table_setcolumndescriptors( descriptors );
    for (var colid in descriptors) {
      thetable.sortable_column(colid);
    }
  }

 }) (tableFactory, jQuery);


// End of file
