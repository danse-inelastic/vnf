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
				//var data = {"id":idlist[0], "column":idlist[1], "value":escape(val)};
                var data = {"sentry.passwd": "demo", "sentry.username": "demo", "actor": "directdb", "routine": "set", "directdb.tables": "samples", "directdb.id": "C8GCB", "directdb.value": escape(val) }
                console.log(data);

				//s = "../cgi-bin/tabletest/table.cgi" 
				s = "../cgi-bin/vnf/main.cgi"
                jQuery.get(s, data);

            
            }
        }
    ); // returns t

}); 
