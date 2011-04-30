#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os
from pyre.inventory.Inventory import Inventory as InventoryBase

class Mixin(object):


    class Inventory(InventoryBase):

        import luban.inventory

        uploadid = luban.inventory.str('uploadid')


    def onUpload(self, director):
        '''
        uploadid: upload it

        return: new structure id
        '''
        # assumption: only one file uploaded

        # namespace
        import os

        # 
        domaccess = director.retrieveDOMAccessor('atomicstructure')

        # check the upload
        uploadid = self.inventory.uploadid
        # .. get the upload directory
        from vnf.utils.upload import abspath
        dir = abspath(uploadid)
        # .. get the entries
        entries = os.listdir(dir); found = None
        # .. find the entry with the correct ext
        for entry in entries:
            if entry.startswith('.'): 
                continue
            base, ext = os.path.splitext(entry)
            if ext in domaccess.acceptable_datafile_exts:
                found = entry
                break
            continue
        else:
            raise RuntimeError, 'File does not have understandable extension'
        
        # path to the file
        found = os.path.join(dir, found)

        # check if the files are sane and are not hostile
        if not domaccess.datafileIsSane(found):
            raise RuntimeError, "Failed to parse the data file"
        
        #
        newrecordid = domaccess.saveDataFileAsStructure(found)
        
        return newrecordid


# version
__id__ = "$Id$"

# End of file 

