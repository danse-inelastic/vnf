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


// needs 
//   - ajaxupload.3.0.js
//   - elementFactory.js

(function($) {

  $.fn.uploader = function(action, parameters) {
    
    // "this" is the division for the button
    var div = $(this);

    // create the subelments
    var table = elementFactory.createTag('table');
    div.append(table);
    var tbody = elementFactory.createTag('tbody');
    table.append(tbody);
    var tr = elementFactory.createTag('tr');
    tbody.append(tr);
    var buttontd = elementFactory.createTag('td')
    tr.append(buttontd);
    var buttondiv = elementFactory.createTag('div', {'class': 'uploadButtonContainer'});
    buttontd.append(buttondiv);
    var button = elementFactory.createTag('div', {'class': 'uploadButton'})
    buttondiv.append(button);
    var statustd = elementFactory.createTag('td');
    tr.append(statustd);
    var status = elementFactory.createTag('div');
    statustd.append(status);
    
    button.text('Upload');
    
    // the interval callback
    var interval;
    
    new Ajax_upload(button, 
    {action: action, 
     data: parameters,
     name: 'myfile',
     onSubmit : function(file, ext){
	// change button text, when user selects file			
	status.text('Uploading');
	
	// If you want to allow uploading only 1 file at time,
	// you can disable upload button
	this.disable();
			
	// Uploding -> Uploading. -> Uploading...
	interval = window.setInterval(function(){
	    var text = status.text();
	    if (text.length < 13){
	      status.text(text + '.');					
	    } else {
	      status.text('Uploading');				
	    }
	  }, 200);
      },
     onComplete: function(file, response){
	window.clearInterval(interval);
	
	// enable upload button
	this.enable();
	
	// show filename
	status.text("'"+ file +"' uploaded");
      }
    });

  };

 }) (jQuery);


// End of file
