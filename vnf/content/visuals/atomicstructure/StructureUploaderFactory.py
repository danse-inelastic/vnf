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


import luban.content


class Factory(object):
    
    
    upload_handler_actor_name = 'upload'
    upload_handler_routine_name = 'receive_file'

    
    def __init__(self, director=None, oncomplete=None):
        '''oncomplete: a 2-tuple of actor name and routine name to handle oncomplete event
        '''
        self.director = director
        self.oncomplete = oncomplete
        return


    def build(self):
        director = self.director
        
        # container
        doc = luban.content.document(title='', Class='container', id='structure-uploader-container')

        # 
        doc.paragraph(text=['Choose a file to upload.  Supported formats are:'])

        doc.paragraph(text=['1) .cif'])

        doc.paragraph(text=['2) .pdb'])
        doc.paragraph(text=['3) .pdffit'])
        doc.paragraph(text=['4) .xyz',
         'Each line must contain an atom symbol followed by its position.',    
         'If 9 floats are given on the comment line, these are used as the lattice vectors.',
         'Format: a_x a_y a_z b_x b_y b_z c_x c_y c_z'])
        doc.paragraph(text=['5) .xyz (VNF format)',
         'All previous xyz rules apply, except an additional charge (in electron units) may be given following each position triplet.'])
        doc.paragraph(text=['6) .xyz (raw)',
         'Each line must contain an atom symbol followed by its position.',
         'No total number of atoms is required.'])

        # spacer
        doc.paragraph()

        # uploader
        uploader = luban.content.uploader(
            name = 'structureUploader',
            label='Click here to browse for the structural file to upload',
            )        
        doc.add(uploader)

        # upload handler
        uploadid = director.getGUID() # identifier of this upload
        saveuploadfile = luban.content.load(
            actor=self.upload_handler_actor_name, 
            routine=self.upload_handler_routine_name,
            id=uploadid, 
            )
        uploader.onsubmit=saveuploadfile

        # complete handler
        actor, routine = self.oncomplete
        uploader.oncomplete = luban.content.load(
            actor=actor, routine=routine,
            uploadid = uploadid)

        # spacer
        doc.paragraph()

        return doc


# version
__id__ = "$Id$"

# End of file 

