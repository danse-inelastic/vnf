/*
 * Copyright (c) 2008 Greg Weber greg at gregweber.info
 * Dual licensed under the MIT and GPL licenses
 *
 * jquery plugin
 * make an html table editable by the user
 *   user clicks on a cell, edits the value,
 *   then presses enter or clicks on any cell to save the new value
 *   pressing escape returns the cell text to its orignal text
 *
 * documentation at http://gregweber.info/projects/uitableedit
 * 
 * var t = $('table')
 * $.uiTableEdit( t ) // returns t
 *
 * options : off, mouseDown, find, dataEntered, dataVerify, editDone
 *   off : turns off table editing
 *   find : defaults to tbody > tr > td
 *   mousedown : called in context of the table cell (as a normal event would be)
 *     if mouseDown returns false, cell will not become editable
 *   dataVerify : called in context of the cell,
 *     if dataVerify returns false, cell will stay in editable state
 *     if dataVerify returns text, that text will replace the cell's text
 *     arguments are the cell's text, original text, event, jquery object for the cell
 *   editDone : invoked on completion
 *     arguments: td cell's new text, original text, event, and jquery element for the td cell
*/

var cid_date    = new Array();
var link_html	= new Array();
var click_delay = 1200;

jQuery.uiTableEdit = function(jq, options)
{
	// Do I really need to unbind both mouseup and mousedown?
	function unbind()
	{
		// jq.find( options.find ) returns all cells with tag <td> that are found in the path 'tbody > tr > td'
		tds = jq.find( options.find )
		tds.unbind('mousedown.uiTableEdit')
		tds.unbind('mouseup.uiTableEdit')
		return tds
	}

	function unbind_mousedown()
	{
		return jq.find( options.find ).unbind('mousedown.uiTableEdit')
	}

	function unbind_mouseup()
	{
		return jq.find( options.find ).unbind('mouseup.uiTableEdit')
	}

	options = options || {}
	options.find = options.find || 'tbody > tr > td'
	if( options.off ){
		unbind().find('form').each( function(){ var f = $(this);
		f.parents("td:first").text( f.find(':text').attr('value') );
		f.remove();
		});
		return jq;
	}
	
	function bind_mouse_down( mouseDn )
	{
		unbind_mousedown().bind('mousedown.uiTableEdit', mouseDn ) // mousedown.uiTableEdit
	}
	
	function bind_mouse_up( mouseUp )
	{
		unbind_mouseup().bind('mouseup.uiTableEdit', mouseUp ) // mousedown.uiTableEdit
	}

	// Get now UNIX time
	function _get_time_now()
	{
		var mydate = new Date();
		return mydate.getTime(); 
	}

	 function td_edit(){
		var td = jQuery(this);
		var cid = this.attr('id'); // ID of the current <td> tag
		function has_single_a_tag()
		{
			// Doesn't handle properly where there are white spaces outside <a> tag.
			// It just trims the spaces :)
			btext = td.text(); 
			return (td.find('a').length === 1 && td.text().replace(/^\s*|\s*$/g,'') == td.find('a')[0].text) ? true : false;
		}

		a_tag = has_single_a_tag();

		atag = $('#'+cid+' > a'); //1. Save <a> element
		//console.log($('#'+cid+' > a').text());
		
		function update_text(val)
		{
			td.empty();
			td.append(atag); //2. Append to <td>
			if (has_single_a_tag())
			{
				atag.text(val); //td.find('a').each(function(){$(this).text(val)});
				//console.log("has_single_a_tag");
			}
			else
			{
				td.text( val );
			}

		}
		function restore(e)
		{
			var val = td.find(':text').attr('value')
			// Verify data first!
			if( options.dataVerify ){
				var value = options.dataVerify.call(this, val, orig_text, e, td);
				if( value === false ){ return false; }
				if( value !== null && value !== undefined ) val = value;
			}
			update_text(val);
			if( options.editDone ) options.editDone(val,orig_text,e,td)
			bind_mouse_down( mousedown_wrapper );
		}
	
		function checkEscape(e)
		{
			if (e.keyCode === 27) 
			{
				update_text(orig_text);
				bind_mouse_down( mousedown_wrapper );
			}
		}

		var orig_text = td.text();
		//console.log(has_single_a_tag());
		var w = td.width();
		var h = td.height();

		td.css({width: w + "px", height: h + "px", padding: "0", margin: "0"});
		td.html( '<form name="td-editor" action="javascript:void(0);">' + 
		'<input type="text" name="td_edit" value="' +
		td.text().replace( /"/g, '&quot;') + '" style="margin:0px;padding:0px;border:0px;width: ' +
		w  + 'px;"></input></form>' ) 
		.find('form').submit( restore ).mousedown( restore ).blur( restore ).keypress( checkEscape ); //height:' + h + 'px;

		function focus_text(){ td.find('input:text').get(0).focus() }
	
		// focus bug (seen in FireFox) fixed by small delay
		setTimeout(focus_text, 50);
		
		/* TODO: investigate removing bind_mouse_down
		I also got rid of bind_mouse_down(restore),
		because now that you can refocus on fields that have been blurred,
		you can have multiple edits going simultaneously
		*/
		bind_mouse_down( restore );
	} // End of td_edit()

	event_timer = function (cid)
	{
		obj = $('#'+cid) // Find the td object again based on id!

		var timenow = _get_time_now(); // Get time now
		//console.log(timenow+' - '+cid_date[cid]);
		if ( timenow > 0 && cid_date[cid] > 0 && ( (timenow - cid_date[cid] ) > click_delay ) )
		{
			console.log("td_edit");
			cid_date[cid] = 0; //Wipe tid time and convert
			td_edit.apply(obj, arguments);
			//td_edit.apply(this, arguments);
			return false;
		}
		
		if (  cid_date[cid] > 0 ) //Not wiped? loop on!
		{
			setTimeout( "event_timer('"+cid+"')", 5 );
		}
		else
		{
			return false;
		}
	}
	function event_mousedown()
	{
		var cid = this.id; // Cell ID: <td id="some_id">
		// Enter edit mode only if the <td> has id attribute and it is not empty
		if (cid !== '')
		{
			cid_date[cid] = _get_time_now(); // Start timer
			setTimeout( "event_timer('"+cid+"');", 5 );
		}

	}

	function event_mouseup()
	{
		cid = this.id;
		cid_date[cid] = 0; // Reset timer
		console.log("event_mouseup");
	}

	var mousedown_wrapper = !options.mouseDown ? event_mousedown : function(){ //event_mousedown
		if( options.mouseDown.apply(this,arguments) == false ) return false; // If function options.mouseDown is implemented
		//td_edit.apply(this,arguments);
	};
	var mouseup_wrapper = !options.mouseUp ? event_mouseup : function(){
		if( options.mouseUp.apply(this,arguments) == false ) return false; // If function options.mouseUp is implemented
	};

	bind_mouse_up( mouseup_wrapper );
	bind_mouse_down( mousedown_wrapper );
	return jq;
}
