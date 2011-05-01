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
        doc = luban.content.document(
            title='Upload an atomic structure', 
            Class='container', 
            id='structure-uploader-container')

        # 
        # sp = doc.splitter()
        grid = luban.content.grid(); doc.add(grid)
        row = grid.row()
        
        # left: uploader
        uploader = self.createUploadButton()
        # sp.section(id='left').add(uploader)
        row.cell(id='left').add(uploader)

        # right: link to show hints
        # .. first we need the hints document
        hintsdoc = luban.content.document(
            id='structure-uploader-hints-doc',
            hidden = True,
            )
        # .. then create the link
        showhints = luban.content.select(element=hintsdoc).show()
        hintlink = luban.content.link(
            id = 'structure-uploader-hint-link',
            onclick = showhints,
            label = 'Show me supported file formats',
            )
        # .. and add it to the right 
        # sp.section(id='right').add(hintlink)
        row.cell(id='right').add(hintlink)
        
        # content of hints
        doc.add(hintsdoc)
        rstdoc = luban.content.rstdoc(id='structure-uploader-explanation')
        hintsdoc.add(rstdoc)
        rstdoc.text = [
            'Supported formats are:',
            '',
            '* .cif',
            '* .pdb',
            # '* .pdffit',
            '* .xyz',
            '',
            '  Each line must contain an atom symbol followed by its position.',    
            '  If 9 floats are given on the comment line, these are used as the lattice vectors.',
            '  Format::',
            '',
            '    a_x a_y a_z b_x b_y b_z c_x c_y c_z',
            '* .xyz (VNF format)',
            '',
            '  All previous xyz rules apply, except an additional charge (in electron units) may be given following each position triplet.',
            '* .xyz (raw)',
            '',
            '  Each line must contain an atom symbol followed by its position.',
            '  No total number of atoms is required.',
            ]
        rstdoc.hidden = True

        # spacer
        # doc.paragraph()

        return doc


    def createUploadButton(self):
        director = self.director
        
        # uploader
        uploader = luban.content.uploader(
            name = 'structureUploader',
            label='Browse for the structural file to upload',
            Class = 'big-button',
            )        

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

        return uploader


# version
__id__ = "$Id$"

# End of file 

