# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



class Instrument(object):

    components = []

    category = ''

    name = ''
    short_description = ''
    long_description = ''

    def hasSampleComponent(self):
        "checks whether this instrument has a 'sample' component"
        from neutron_components.SampleComponent import SampleComponent
        for component in self.components:
            if isinstance(component, SampleComponent):
                return True
            continue
        return False
    

    pass # end of Instrument



from AbstractNeutronComponent import AbstractNeutronComponent
from neutroncomponent_types import getTypes
neutroncomponent_types = getTypes()


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    components = InvBase.d.referenceSet(
        name = 'components',
        targettype=AbstractNeutronComponent, targettypes=neutroncomponent_types,
        owned = 1)
    
    category = InvBase.d.str(name = 'category', max_length = 64)

    name = InvBase.d.str(name='name')
    short_description = InvBase.d.str(name='short_description')
    long_description = InvBase.d.str( name = 'long_description', max_length = 8192 )

    dbtablename = "instruments"

Instrument.Inventory = Inventory
del Inventory


from _ import o2t, AbstractOwnedObjectBase
InstrumentTable = o2t(Instrument, {'subclassFrom': AbstractOwnedObjectBase})


import dsaw.db
InstrumentTable.addColumn(dsaw.db.varchar(name='status', length=32, default='online'))
InstrumentTable.addColumn(dsaw.db.boolean(name='has_sample_component'))



# ????
def inittable(db):
    from instruments import initall
    return initall(db)


# version
__id__ = "$Id$"

# End of file 
