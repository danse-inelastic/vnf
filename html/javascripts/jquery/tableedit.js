var clickFlag = false;

jQuery(document).ready(function(){ 
    jQuery(".tablesorter").tablesorter(); 
    var t = jQuery('#tablesorter-demo');
    jQuery.uiTableEdit( t , 
        {
            editDone : function(val,orig_text,ev, el){
                console.log(val);//
                console.log(orig_text);//

				// Get id of the tag <td> and split it to array [idNumber, columnNumber]
				var idlist = jQuery(el).attr('id').split("_");
				//var val
				console.log(idlist);
				
                var thead = jQuery("thead>tr>",t);
                console.log(thead);//
				var data = {"id":idlist[0], "column":idlist[1], "value":escape(val)};
                console.log(data);
				// Restore when debugged!
                jQuery.get("../cgi-bin/tabletest/table.cgi", data);

            
            }
        }
    ); // returns t

	// Additional function calls
/*
	$(this).click(function(){
		clickFlag = true;
		//if (clickFlag === true){
		alert("Click");
		clickFlag = false;
		//}
	});
	
	$(this).mousedown(function(){
		setTimeout(function(){
		if (!clickFlag){
			alert('Mouse down');
		};
		},
		5000);
	});
*/
}); 

// Junk code:

/*
                var data = [];
                data.push("id="+idlist[0]);
                data.push("column="+idlist[1]);
                data.push("value="+escape(val));
                
                //var row = jQuery(el).parent().children();
                //console.log(row);
                /*
                row.each(
                    function(nr){
                        var key = thead.eq(nr).text().replace(" ","_");
                        data.push(key + "=" + escape(jQuery(this).text()));         
                    }
                );
				
                console.log(data);//
                console.log(data.join("&"));
				
                jQuery.ajax({
                        type: "POST",
                        url: "./table.py", //./include/server.php",
                        data: data.join("&"),
                        success: function(msg){
                            console.log(msg);
                        }
                });
*/
