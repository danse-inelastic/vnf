# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def visual(uploadid=None, recordid=None):
    '''
    uploadid: unique id for this upload
    recordid: identifier for the stuff this upload is about
    '''
    doc = lc.document(title='', Class='container')

    # uploader
    uploader = lc.uploader(
        name = 'myupload',
        label='Click here to browse the XXX file to upload',
        )
    
    # action to save upload
    saveuploadfile = lc.load(
        actor='upload', routine='receive_file',
        id=uploadid, # identifier of this upload
        )
    # .. assign it to uploader
    uploader.onsubmit=saveuploadfile
    
    # action when upload is complete
    uploader.oncomplete = lc.load(
        actor='myactor', routine='onUpload',
        uploadid = uploadid,
        recordid = recordid)

    # 
    doc.add(uploader)

    return doc


# version
__id__ = "$Id$"

# End of file 
