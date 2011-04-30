.. _vnfdeveloperguideui:

User interface
==============

User interfaces of VNF is implmented using luban: http://luban.danse.us.
Luban has a detailed documentation page at 
http://docs.danse.us/pyre/luban/sphinx/Documentation.html , in which
of particular interests are its API
http://docs.danse.us/pyre/luban/sphinx/API.html ,
and the demo of the API at
http://luban.danse.us/aokuang

Following are documentation of some aspects of luban that are
especially relevant in VNF.

Widgets
-------


Downloader
""""""""""
When creating a downloader, you will need a label and a load action.
The routine that handles the load action must return a
luban.content.File.File object. 

A demo is available at 
http://luban.danse.us/cgi-bin/aokuang/main.cgi?actor=downloader 

Please click on the "Code" tab there to see how you can
implement a downloader.


Uploader
""""""""

See vnf/content/visuals/uploader_example for an example.

