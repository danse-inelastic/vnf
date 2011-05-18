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



class ARCSIQEResolutionComputation:

    Q = 10.
    E = 50.
    dQ = 0.
    dE = 0.
    ncount = 1e8
    # neutron storage that has neutrons at ARCS sample position
    neutronsatsample = None
    
    # key properties
    # if values for key properties are the same, the two
    # objects can be regarded as the same
    key_props = [
        'Q', 'E', 'dQ', 'dE',
        'ncount',
        'neutronsatsample',
        ]
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = [
            'Q',
            'E',
            'dQ',
            'dE',
            'ncount',
            'neutronsatsample',
            ]
        #
        def _createfield_for_neutronsatsample(obj):
            # this is a method of mold.
            self = drawer.mold

            # imports
            import luban.content 
            from luban.content.FormSelectorField import FormSelectorField
            
            # utils
            orm = self.orm

            # data 
            record = self.orm(obj)
            referred_record = record.neutronsatsample and record.neutronsatsample.id \
                              and record.neutronsatsample.dereference(self.orm.db)

            # widget
            doc = luban.content.document(Class='container', id='neutronsatsample-selector-container')
            sp = doc.splitter()
            left = sp.section(); right = sp.section()
            #
            selector = FormSelectorField(label='beam profile:', name='neutronsatsample')
            left.add(selector)

            # default selection
            if referred_record:
                value=orm.db.getUniqueIdentifierStr(referred_record)
            else:
                value=None

            # choices
            #  get matter
            entries = luban.content.load(
                actor='orm/arcsiqeresolutioncomputations',
                routine='getSelectorEntriesForBeamProfile',
                id = record.id,
                # include_none_entry = 1,
                )
            selector.oncreate = luban.content.select(element=selector)\
                .setAttr(entries=entries, value=value)
            
            return doc
        
        drawer.mold._createfield_for_neutronsatsample = _createfield_for_neutronsatsample
        
        return

from ...NeutronStorage import NeutronStorage

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    Q = InvBase.d.float(name='Q', default=8)
    Q.label = 'Momentum transfer (angstrom)'
    Q.validator = InvBase.v.isBoth(InvBase.v.greaterEqual(0), InvBase.v.less(1000))
    
    dQ = InvBase.d.float(name='dQ', default=0)
    dQ.label = 'Momentum transfer range (angstrom)'
    dQ.validator = InvBase.v.greaterEqual(0)
    
    E = InvBase.d.float(name='E', default=70)
    E.label = 'Energy transfer (meV)'
    E.validator = InvBase.v.isBoth(InvBase.v.greaterEqual(0.1), InvBase.v.less(1e5))
    
    dE = InvBase.d.float(name='dE', default=0)
    dE.label = 'Energy transfer range (meV)'
    dE.validator = InvBase.v.greaterEqual(0)
    
    ncount = InvBase.d.int(
        name='ncount', default=10000000,
        validator = InvBase.v.greaterEqual(1000000),
        )
    ncount.label = 'number of Monte Carlo simulation runs' #. Each MC run corresponds to 34kJ energy.'
    ncount.expert = True
    
    neutronsatsample = InvBase.d.reference(
        name='neutronsatsample', targettype=NeutronStorage, owned=0)

    dbtablename = 'arcsiqeresolutioncomputations'


ARCSIQEResolutionComputation.Inventory = Inventory

from vnf.dom._ import o2t
from vnf.dom.Computation import Computation
ARCSIQEResolutionComputation_Table = o2t(ARCSIQEResolutionComputation, {'subclassFrom': Computation})
ARCSIQEResolutionComputation_Table.job_builder = 'mcvine/arcs/iqe-resolution'
ARCSIQEResolutionComputation_Table.actor = 'instruments/arcs/iqe-resolution'
ARCSIQEResolutionComputation_Table.result_retriever = 'mcvine/arcs/iqe-resolution'


# version
__id__ = "$Id: ARCSIQEResolutionComputation.py 3744 2011-04-28 06:17:57Z linjiao $"

# End of file 
