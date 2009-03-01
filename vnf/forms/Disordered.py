# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnf.components.Form import Form as base
from vnf.components.Actor import actionRequireAuthentication, action_link
from vnf.components.DBObjectForm import formactor_action_prefix

class Disordered( base ):

    class Inventory( base.Inventory ):

        import pyre.inventory as inv
        
        disorderedId = inv.str( 'disorderedId', default = '' )
        
        chemical_formula = inv.str('chemical_formula', default = '' )
        chemical_formula.meta['tip'] = 'A short description'
        
        listOfAtoms = inv.str('listOfAtoms')
        
        ax = inv.str('ax',default = '1.0')
        ay = inv.str('ay',default = '0.0')
        az = inv.str('az',default = '0.0')
        bx = inv.str('bx',default = '0.0')
        by = inv.str('by',default = '1.0')
        bz = inv.str('bz',default = '0.0')
        cx = inv.str('cx',default = '0.0')
        cy = inv.str('cy',default = '0.0')
        cz = inv.str('cz',default = '1.0')
        
#    record = None
        
#    def __init__(self):
#        base.__init__(self)
#        self.dbRecord = None

    def expand(self, form, errors = None, properties = None, disorderedId = '', 
               showimportwidget=False):
        '''expand an existing form with fields from this component'''
        # the strategy is to create a new object of a given class if it does not exist
        # and look up one if it already exists.  it's existence is based on whether an id
        # is passed in the function argument
        prefix = formactor_action_prefix
        director = self.director        
        
        if not disorderedId:
            tableClass = director.clerk._getTable(materialType)
            record = director.clerk.newOwnedObject(tableClass)
            disorderedId = self.inventory.disorderedId = record.id
        else:
            record = director.clerk.getRecordByID('disordered', disorderedId)
            self.inventory.disorderedId = record.id

        self.chemical_formula = form.text(
            id='text1', name='%s.chemical_formula'%prefix,
            label='Matter Description', value = record.chemical_formula)

        if showimportwidget:
            p = form.paragraph()
            p.text = ['Import the sample from a database:']
            p = form.paragraph()
            # !!! need a better way to specify java action
            p.text = ['<a href="java/cod2.jnlp"><img src="images/CodPicture.gif" alt="CodUI"/></a>']        
        
            p = form.paragraph()
            p.text = ['or input material parameters manually:']
            
        box = form.box()

        cartesian_lattice = record.cartesian_lattice
        import numpy
        cartesian_lattice = numpy.array(cartesian_lattice)
        cartesian_lattice.shape = 3,3
        a, b, c = cartesian_lattice
        
        self.ax = box.text(id='ax', name='%s.ax' % prefix, label='a: (x)', 
                      value = a[0]) 
        self.ay = box.text(id='ay', name='%s.ay' % prefix, label='(y)', 
                      value = a[1]) 
        self.az = box.text(id='az', name='%s.az' % prefix, label='(z)', 
                      value = a[2]) 
        box = form.box()
        self.bx = box.text(id='bx', name='%s.bx' % prefix, label='b: (x)', 
                      value = b[0])
        self.by = box.text(id='by', name='%s.by' % prefix, label='(y)', 
                      value = b[1])   
        self.bz = box.text(id='bz', name='%s.bz' % prefix, label='(z)', 
                      value = b[2])  
        box = form.box()
        self.cx = box.text(id='cx', name='%s.cx' % prefix, label='c: (x)', 
                      value = c[0]) 
        self.cy = box.text(id='cy', name='%s.cy' % prefix, label='(y)', 
                      value = c[1]) 
        self.cz = box.text(id='cz', name='%s.cz' % prefix, label='(z)', 
                      value = c[2])

        coords = record.fractional_coordinates
        import numpy
        coords = numpy.array(coords)
        coords.shape = -1, 3
        
        listOfAtoms = '\n'.join(
            ['%s\t%s' % (atom, ' '.join([str(x) for x  in pos]))
             for atom, pos 
             in zip(record.atom_symbols, coords)]
            )
        self.listOfAtoms = form.textarea(
            id='listOfAtoms', name='%s.listOfAtoms' % prefix, 
            label='List of atoms (i.e. H  0.0  0.0  0.5)', rows=20, 
            default = listOfAtoms)
          
    def processUserInputs(self):   
        '''process user inputs for material and save them to db
        commit: if true, commit to database record. 
        '''
        
        director = self.director
        
        try: # first try to get a record with the inventory id from the db
            record = director.clerk.getRecordByID('disordered', self.inventory.disorderedId)
        except: # if can't find, create a new one
            tableClass = director.clerk._getTable('disordered')
            record = director.clerk.newOwnedObject(tableClass)
            self.inventory.disorderedId = record.id
      
        record.chemical_formula = self.inventory.chemical_formula

        a = map(float,[self.inventory.ax, self.inventory.ay, self.inventory.az])
        b = map(float,[self.inventory.bx, self.inventory.by, self.inventory.bz])
        c = map(float,[self.inventory.cx, self.inventory.cy, self.inventory.cz])
        #lattice=a+b+c
        record.cartesian_lattice = a+b+c#lattice
        
        atoms = []; coords = []
        listOfAtoms = self.inventory.listOfAtoms
        for line in listOfAtoms.split('\n'):
            tokens = line.split()
            if len(tokens) != 4: continue
            atoms.append(tokens[0])
            coords.append([eval(i) for i in tokens[1:4]])
        record.atom_symbols = atoms
        import numpy
        coords = numpy.array(coords)
        coords.shape = -1,
        record.fractional_coordinates = list(coords)
            
        self.director.clerk.updateRecord(record)
        return record
    
formactor_action_prefix = 'actor.form-received' # assumed actor is a form actor


# version
__id__ = "$Id$"

# End of file 
