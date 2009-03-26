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



(function($) {

  $.autorefresh_start = function (timeout) {
    $.autorefresh_seconds_remained = timeout;
    $.autorefresh_update();
  };
  
  $.autorefresh_update = function () {

    if ($.autorefresh_seconds_remained==1) {
      window.location.reload();
    } else {
      $.autorefresh_seconds_remained -= 1;
      window.status=timestr($.autorefresh_seconds_remained);
      // wait 1 second to refresh
      setTimeout("$.autorefresh_update()",1000);
    }
  };

  // data
  $.autorefresh_seconds_remained = 0;

  // helpers
  function timestr(seconds) {
    curmin=Math.floor(seconds/60);
    cursec=seconds%60;
    if (curmin!=0)
      curtime=curmin+" minutes and "+cursec+" seconds left until page refresh!";
    else
      curtime=cursec+" seconds left until page refresh!";
    return curtime;
  }

 }) (jQuery);

