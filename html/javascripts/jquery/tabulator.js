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


// tabulator


// some meta data are saved in cells to allow sorting, formatting.
// some other meta data are stored in table.data('column_descriptors')
// 
// columns are identified by their ids (string).
// rows are identified by their ids (usually numbers).
// 
// The last row in the table head is regarded as the row that 
// describes the columns in the table. 
// The attribute 'id' of a cell in that row is regarded as the
// id of the column.
// A cell in that column will have an attribute "colid" and
// it should be the same as the column id.
//
// Right now, there is no way to know "row number" given a row.
// This might cause trouble if you need to know, for example, what is
// the cell above or below a given cell.
// But, what would be the use case? Running balance could be one, but
// do we really care?

// todo:
//  UI 
//   1. add a new row, delete existing row ( google map for example )
//   2. resizable columns (less important)
//   3. numeric cell should allow calculator
//   4. locale ( for calendar and money, for example )
//  talking to server
//   1. ajax?


(function($) {

  // ********************************************
  //  public methods added to jQuery
  // ********************************************

  // ---------------------
  // table meta data setup
  // ---------------------

  // set column descriptors for a table
  // a column descriptor describe the properties of a column, such
  // as name, type, sorting direction? 
  $.fn.table_setcolumndescriptors = function ( descriptors ) {
    $(this).data( 'column_descriptors', descriptors );
  };



  // ---------------------
  // table manipulations
  // ---------------------

  // sort a table by a column
  // this -> table
  $.fn.sort_table_by_col = function( colid, direction ) {

    // save rows before we remove them from the table
    var saverows = [];
    var body = get_tablebody( this );
    var rows = body.children();
    for (var i = 0; i<rows.length; i++) {
      row = rows[i];
      saverows.push( row );
    }
    body.empty();
    
    column_descriptors = this.data('column_descriptors');
    var newrows = sort_rows_by_col( saverows, colid, column_descriptors, direction );
    
    for (var i=0; i<newrows.length; i++) {
      body.append( newrows[i] );
    }
  };
  

  // make a cell editable
  $.fn.enable_cell_editing = function ( callback ) {
    
    enable_cell_editing_by_datatype( this );

    // when cell lost focus, we should quit editing mode

    //  "input" or "select"?
    var input = this.children( 'input' );
    if (input.length == 0) input = this.children( 'select' );

    //  focus on input now
    input.focus();
    
    //  
    var cell  = this;
    cell.bind( "restore_from_editing", function() {
	cell.restore_cell_from_editing();
	if (callback) callback( cell );
	cell.unbind( "restore_from_editing" );
      } );
  };

  
  // restore a cell from editable to normal
  $.fn.restore_cell_from_editing = function () {
    restore_cell_from_editing_by_datatype( this );
  }
  

  // extract data value from a cell
  $.fn.extract_data_from_cell = function () {
    cell = this;
    datatype = cell.attr( 'datatype' );
    var handler = eval( '$.fn.extract_data_from_cell.handle_' + datatype );
    return handler( cell );
  };


  // establish a cell given a new value
  $.fn.establish_cell_from_data = function( data ) {
    cell = this;
    datatype = cell.attr( 'datatype' );
    var handler = eval( '$.fn.establish_cell_from_data.handle_' + datatype );
    return handler( cell, data );
  };


  // get value from an editing widget for a cell
  $.fn.cell_value_from_editing_widget = function() {
    cell = this;
    datatype = cell.attr( 'datatype' );
    var handler = eval( '$.fn.cell_value_from_editing_widget.handle_' + datatype );
    return handler( cell );
  };


  // ---------------------
  // basic table creation
  // ---------------------

  // append a row to the end of the table body. 
  // only the data are specified. meta data 
  // will be obtained from "column_descriptors" that is attached to the table
  //
  //   table_appendrow_dataonly( rowid, [cell0, cell1, ...] )
  //
  $.fn.table_appendrow_dataonly = function(rowid, datalist) {

    var tbl = this;

    var ncells = datalist.length;
    
    var column_descriptors = tbl.data( 'column_descriptors' );

    row = append_newrow_to_table( tbl, rowid );

    fill_row_with_data( row, datalist, column_descriptors );
  };


  // insert a row to the table body after the row for which the row id is given.
  // only the data are specified. meta data 
  // will be obtained from "column_descriptors" that is attached to the table
  //
  //   table_insertrowafter_dataonly( 'row2a', 'row2', [cell0, cell1, ...] )
  //
  // newrowid: id of the  row to be inserted
  // rowid: id of the row after which the new row will be inserted
  $.fn.table_insertrowafter_dataonly = function(newrowid, rowid, datalist) {

    var tbl = this;

    var column_descriptors = tbl.data( 'column_descriptors' );

    row = insert_newrowafter_to_table( tbl, newrowid, rowid );
    if (row == undefined) return;
    
    fill_row_with_data( row, datalist );
  };



  // ********************************************
  // handlers
  // These handlers can be extended so that the
  // behaviors of this tabulator can be changed
  // ********************************************


  // --------------------------------------
  // handlers to extract data from a cell
  // --------------------------------------
  // text
  $.fn.extract_data_from_cell.handle_text = function( cell ) {
    return cell.text();
  };
  
  // money
  $.fn.extract_data_from_cell.handle_money = function( cell ) {
    $amount = $(cell.children( 'span.moneyAmount' )[0]);
    amount = $amount.text();
    return Number( amount );
  };
  
  // --------------------------------------
  // handlers to establish a cell from data
  // --------------------------------------
  //  text
  $.fn.establish_cell_from_data.handle_text = function( cell, value ) {
    return cell.text( value ); 
  };
  
  //  date
  $.fn.establish_cell_from_data.handle_date = function( cell, value ) {
    return cell.text( value ).addClass( "date" );
  };
  
  //  boolean
  $.fn.establish_cell_from_data.handle_boolean = function( cell, value ) {
    var checked = Number(value)==0? '':'checked="checked"';
    var html = '<input type="checkbox" ' + checked + ' />';
    cell.css( 'text-align', 'center' );
    return cell.html( html ); 
  };
  
  //  money
  $.fn.establish_cell_from_data.handle_money = function( cell, value ) {
    html = '<span class="moneyCurrencySymbol">$ </span>';
    html += '<span class="moneyAmount">' + value + '</span>';
    cell.css( 'text-align', 'right' );
    cell.html( html );
  };

  //  updown
  $.fn.establish_cell_from_data.handle_upanddown = function( cell, value ) {
    cell.text( value );
    if (value > 0) 
      return cell.css("color", "green").prepend( '^' );
    else
      return cell.css("color", "red").prepend( 'v' );
  };

  // single_choice
  $.fn.establish_cell_from_data.handle_single_choice = function( cell, value ) {
    column_descriptor = get_column_descriptor( cell );
    choices = column_descriptor.choices;
    text = choices[ value ];
    cell.text( text );
    return cell;
  };  

  //  single choice in one column
  $.fn.establish_cell_from_data.handle_single_choice_in_one_column = function( cell, value ) {
    var html = '<input type="radio" ';
    var checked = Number(value)==0? '':'checked="checked"';
    html += checked;
    html += 'name="' + cell.attr('name') + '"';
    html += '/>';
    cell.css( 'text-align', 'center' );
    return cell.html( html ); 
  };

  

  // -----------------------------
  // handlers to compare two cells
  // -----------------------------
  //  money
  $.fn.sort_table_by_col.handle_money = function( value1, value2 ) {
    return value1 - value2;
  };

  //  text
  $.fn.sort_table_by_col.handle_text = function( value1, value2 ) {
    return value1.substring(0,1).toLowerCase() < value2.substring(0,1).toLowerCase()? -1: 1;
  };

  // **** need more compare handlers here
  

  // --------------------------------
  // handlers to make a cell editable
  // --------------------------------
  //  text
  $.fn.enable_cell_editing.handle_text = function( cell ) {
    var text = cell.text();
    var width = cell.width();
    var height = cell.height();
    var html = '<input type="text" value ="' + text + '" />'; 
    cell.html( html );
    var input = cell.children('input');
    input.width( width );
    input.height( height );

    input.blur( function () {
	cell = $(this).parent();
	cell.trigger( 'restore_from_editing' );
      } )

    input.bind( 'keydown',  function (e) {
	input = $(this);
	if (e.which != 13 && e.which != 10 ) return true;
	cell = $(this).parent();
	cell.trigger( 'restore_from_editing' );
      } )

  };

  //  date
  $.fn.enable_cell_editing.handle_date = function( cell ) {
    colid = get_column_id( cell );
    var text = cell.text();
    var width = cell.width();
    var height = cell.height();
    input = $('<input class="date-pick"/>');
    cell.html( input );

    descriptor = get_column_descriptor( cell );
    range = descriptor.valid_range;
    startDate = range[0]; endDate = range[1]

    input
    .datePicker( {createButton:false, startDate: startDate, endDate: endDate } )
    .data( 'saved-date', text )
    .dpSetSelected( text )
    .bind( 'dateSelected', function(e, selected) {
	$this = $(this);
	date = selected.asString();
	$this.attr( 'value', date );
	parent = $this.parent();
	parent.trigger( 'restore_from_editing');
      } )
    .bind( 'dpClosed', function( ) {
	$this = $(this);
	date = $this.data( 'saved-date' );
	$this.attr( 'value', date );
	parent = $this.parent();
	parent.trigger( 'restore_from_editing');
      } )
    .dpDisplay()
    ;

    input.width( width );
    input.height( height );
  };

  //  money
  $.fn.enable_cell_editing.handle_money = function( cell ) {
    var amount = cell.extract_data_from_cell();

    var width = cell.width();
    var height = cell.height();
    var html = '<input type="text" value ="' + amount + '" />'; 
    
    cell.html( html );
    var input = cell.children('input')
    input.width( width );
    input.height( height );
    cell.data( 'saved-value', amount );

    input.bind( 'blur',  function () {
	cell = $(this).parent();
	cell.trigger( 'restore_from_editing' );
      } )
    input.bind( 'keydown',  function (e) {
	input = $(this);
	if (e.which != 13 && e.which != 10 ) return true;
	cell = $(this).parent();
	cell.trigger( 'restore_from_editing' );
      } )
  };

  //  single_choice
  $.fn.enable_cell_editing.handle_single_choice = function( cell ) {
    var text = cell.text();
    var width = cell.width();
    var height = cell.height();
    var choices = cell.data( 'choices' );
    if (choices == undefined) {
      descriptor = get_column_descriptor( cell );
      choices = descriptor.choices;
    }
    
    var options = [];
    
    for (var index in choices) {
      var choice = choices[index];
      var  opt = {'value': index, 'text': choice}
      if (choice == text) opt.selected = 'selected';
      options.push( opt );
    }

    var dl = dropdownlist( options );

    cell.html( dl );

    dl.width( width );
    dl.height( height-2 );

    dl.blur( function () {
	cell = $(this).parent();
	cell.trigger( 'restore_from_editing' );
      } )

    dl.change( function () {
	cell = $(this).parent();
	cell.trigger( 'restore_from_editing' );
      } )

  };

  // dropdownlist( [ {'value': "volvo", 'text': "Volvo"}, ... ] )
  function dropdownlist( options ) {
    var html = '<select>';

    for (var i=0; i<options.length; i++) {
      var opt_info = options[i];
      var tmp = '<option value="' + opt_info.value + '" ';

      if (opt_info.selected) tmp += 'selected="selected"';
      
      tmp += '>' ;
      tmp += opt_info.text + '</option>';
      
      html += tmp;
    } 
    
    html += '</select>';
    
    return $(html);
  }


  // ---------------------------------------------
  // handlers to extract value from editing widget
  // ---------------------------------------------
  //  text
  $.fn.cell_value_from_editing_widget.handle_text = function( cell ) {
    return cell.find( "input" ).attr( 'value' );
  };

  //  date
  $.fn.cell_value_from_editing_widget.handle_date = function( cell ) {
    input = cell.find( "input ");
    value = input.attr('value');
    return value;
  };

  //  money
  $.fn.cell_value_from_editing_widget.handle_money = function( cell ) {
    input = cell.find( "input" )
    value = input.attr( 'value' );
    value = Number(value);
    if (value != undefined && value != '' && value != 'undefined' ) return value;
    return cell.data( 'saved-value' );
  };

  //  single_choice
  $.fn.cell_value_from_editing_widget.handle_single_choice = function( cell ) {
    var select = cell.find( "select" );
    return select.attr('value');
  };


  // ********************************************
  // implementation details
  // ********************************************


  // append a row with empty cells to the table and assign an id
  function append_newrow_to_table( table, rowid ) {
    var column_ids = get_column_ids( table );

    var tbody = get_tablebody( table );
    rowindex = tbody.children( 'tr' ).length;

    row = new_row( rowid, rowindex, column_ids );
    tbody.append( row );
    return row;
  }


  // insert a row with empty cells to the table
  // newrowid: the id of the new row 
  // rowid: the id of the row after which the new row will be inserted
  function insert_newrowafter_to_table( table, newrowid, rowid ) {

    var column_ids = get_column_ids( table );

    var tbody = get_tablebody( table );

    rows = tbody.children( 'tr' );
    rowindex = find_row_index( rowid, rows );

    // "after"
    rowindex += 1;

    row = new_row( newrowid, rowindex, column_ids );
    tbody.append( row );
    return row;
  }


  // find row given row id and return row index
  function find_row_index( rowid, rows ) {
    for (i = 0; i<rows.length; i++) {
      row = rows[i];
      if (row.attr('rowid') == rowid) return i;
    }
    return undefined;
  }


  // fill a row of cells with given data.
  // descriptors for every columns are given as well.
  function fill_row_with_data( row, datalist, column_descriptors ) {
    
    cells = row.children( 'td' );
    
    for (var i=0; i<datalist.length; i++) {

      cell = $(cells[i]);
      var descriptor = column_descriptors[cell.attr( 'colid' )];
      var datatype = descriptor.datatype;
      var value = datalist[i];
      cell.attr( 'datatype', datatype );
      cell.establish_cell_from_data( value );

    }

  };


  // find the parent table
  function find_parent_table( element ) {
    return $( element.parents( 'table' )[0] );
  }


  // get column id of a cell
  function get_column_id( cell ) {
    return cell.attr( 'colid' );
  }

  // get column descriptor of a cell
  function get_column_descriptor( cell ) {
    table = find_parent_table( cell );
    colid = get_column_id( cell );
    descriptors = table.data('column_descriptors');
    return descriptors[ colid ];
  }
  

  // enable editing for a cell according to the cell's datatype
  function enable_cell_editing_by_datatype( cell ) {
    var datatype = cell.attr('datatype');
    var handler = eval( "$.fn.enable_cell_editing.handle_" + datatype );
    handler( cell );
  }


  // restore cell from editing status according to the cell's datatype
  function restore_cell_from_editing_by_datatype( cell ) {
    value = cell.cell_value_from_editing_widget( );
    cell.establish_cell_from_data( value );
  }


  // create a new row with empty cells
  function new_row(rowid, rowindex, columnids) {
    
    // new row
    var tr = $(document.createElement( 'tr' ));
    var n = columnids.length;

    odd = rowindex % 2;
    tr.addClass( odd? 'odd':'even' );
    tr.attr( 'rowid', rowid );

    for (i=0; i<n; i++) {
      
      cell = $( document.createElement( 'td' ) );
      cell.attr( 'colid', columnids[i]);

      tr.append(cell);

    }
    
    return tr;
  }

  
  function get_tablehead( table ) {
    var theads = table.children( 'thead' );
    var lastthead = theads[ theads.length - 1 ];
    return $(lastthead);
  }
  
  
  function get_column_ids( table ) {
    thead = get_tablehead( table );
    rows = thead.children( 'tr' );
    lastrow = $( rows[ rows.length -1 ] );
    cols = lastrow.children();
    ids = [];
    for (i=0; i<cols.length; i++) {
      id = $(cols[i]).attr( 'id' );
      ids.push( id );
    }
    return ids;
  }

  function get_tablebody( table ) {
    var tbodys = table.children( 'tbody' );
    var lasttbody = tbodys[ tbodys.length - 1 ];
    return $(lasttbody);
  }

  // sort given rows by a column. The column number is given.
  function sort_rows_by_col( rows, column_id, column_descriptors, direction ) {

    descriptor = column_descriptors[ column_id ];
    datatype = descriptor.datatype;

    function find_column_no( column_id, cells ) {
      for (i=0; i<cells.length; i++) {
	cell = cells[i];
	if ($(cell).attr('colid') == column_id ) return i;
      }
      return undefined;
    }

    colno = find_column_no( column_id, $( rows[0] ).children() );
    var compare_handler = eval( "$.fn.sort_table_by_col.handle_" + datatype );

    function compare (row1, row2) {
      var cells1 = $(row1).children('td');
      var cells2 = $(row2).children('td');

      var cell1 = $(cells1[colno]);
      var value1 = cell1.extract_data_from_cell();

      var cell2 = $(cells2[colno]);
      var value2 = cell2.extract_data_from_cell();
      
      // ****** shall we assert datatypes are matched? *******
      
      return compare_handler( value1, value2 );
    }

    rows.sort( compare );
    if (direction!=0) rows.reverse();
    return rows;
  }

 }) (jQuery);


// version
// $Id$

// End of file 
