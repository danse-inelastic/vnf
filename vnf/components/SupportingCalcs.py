#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor


class SupportingCalcs(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        page = director.retrieveSecurePage('supportingCalcs')
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='Supporting Calculations')
    
        # build the sample input form
        p = document.paragraph()
        p.text = ['Simulate the material with atomistic forcefields (powered by GULP/MMTK)<br>',
                  '<a href="/java/GULP.jnlp">Gulp</a><br>',
                  '<a href="/java/cod.jnlp">cod</a><br>']
        
#        atoms = document.form(name='login', legend='Upload xyz file', action=app.cgihome)
#        
#        name = atoms.text(id='name', name='name', label='Sample Name')
#        name.help = 'An identifying name for this sample.'
#        
#        atomFile = atoms.file(id='atomFile', name='atomFile', label='Xyz file containing atoms')
#        atomFile.help = 'Lattice vectors a,b,c should be on comment line in form a_x a_y a_z b_x b_y b_z c_x c_y c_z'
#        
#        submit = atoms.control(name="submit", type="submit", value="submit")
        
        # view the sample (maybe put this on another page after clicking
        # to submit the sample
#        p = document.paragraph()
#        p.text = ['''<script type="text/javascript"> 
#    jmolInitialize("jmol-11.4.RC10"); 
#    jmolApplet(600, "load orthoGraphKH212x12x1.xyz");</script>''']
#        p = document.paragraph()
#        p.text = [
#            '''<strong>Note</strong>: would like to modify material and/or construct overall sample shape here.  
#    It may be advisable to reuse DANSE Python code by Python/Jython 
#    Web Start (http://personalpages.tds.net/~kent37/Python/JythonWebStart.html)'''
#            ]

        return page 


    def __init__(self, name=None):
        if name is None:
            name = "supportingCalcs"
        super(SupportingCalcs, self).__init__(name)
        return








# version
__id__ = "$Id$"

# End of file 
