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


from _ import Phonons, AbstractScatteringKernel as base
class PolyXtalCoherentPhononScatteringKernel(base):

    phonons = None
    Ei = 70.
    max_energy_transfer = 55.
    max_momentum_transfer = 12.5


    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = ['phonons', 'Ei', 'max_energy_transfer', 'max_momentum_transfer']

        #
        def _createfield_for_phonons(obj):
            # this is a method of mold.
            self = drawer.mold

            # imports
            import luban.content as lc
            from luban.content import load, select
            from luban.content.FormSelectorField import FormSelectorField
            
            # utils
            orm = self.orm

            # data 
            record = self.orm(obj)
            referred_record = record.phonons and record.phonons.id \
                              and record.phonons.dereference(self.orm.db)

            # widget
            doc = lc.document(Class='container', id='phonons-selector-container')
            sp = doc.splitter()
            left = sp.section(); right = sp.section()
            #
            selector = FormSelectorField(label='Phonons:', name='phonons')
            left.add(selector)
            #
            plotcontainer = right.document(Class='container')
            #
            loadplot = lambda uid: load(
                actor='orm/phonons', routine='createGraphicalView',
                uid=uid)

            # default selection
            if referred_record:
                value=orm.db.getUniqueIdentifierStr(referred_record)
                plotcontainer.oncreate = select(element=plotcontainer).append(
                    loadplot(value))
            else:
                value=None

            # choices
            #  get matter
            matter = orm.db.dereference(record.matter)
            matterid = matter.id
            #  dynamically load choices
            entries = load(
                actor='orm/atomicstructures',
                routine='getSelectorEntriesForPhonons',
                id = matterid,
                include_none_entry = 1,
                )
            selector.oncreate = select(element=selector).setAttr(entries=entries, value=value)
            selector.onchange = select(element=plotcontainer).replaceContent(
                loadplot(select(element=selector).getAttr('value')))
            
            return doc

        drawer.mold._createfield_for_phonons = _createfield_for_phonons

    pass # end of PolyXtalCoherentPhononScatteringKernel



from _ import AbstractScatteringKernelInventory as InvBase
class Inventory(InvBase):
    
    phonons = InvBase.d.reference(
        name='phonons', targettype=Phonons, owned=0)

    Ei = InvBase.d.float(name = 'Ei', default = 70)
    
    max_energy_transfer = InvBase.d.float(name = 'max_energy_transfer', default = 55.)

    max_momentum_transfer = InvBase.d.float(name = 'max_momentum_transfer', default = 12.5)

    dbtablename = 'polyxtalcoherentphononscatteringkernels'

    pass # end of Inventory


PolyXtalCoherentPhononScatteringKernel.Inventory = Inventory
del Inventory
from _ import o2t, KernelTableBase
PolyXtalCoherentPhononScatteringKernelTable = o2t(
    PolyXtalCoherentPhononScatteringKernel,
    {'subclassFrom': KernelTableBase},
    )


# obsolete
def inittable(db):
    def k(id, phonons, Ei, max_energy_transfer, max_momentum_transfer):
        r = PolyXtalCoherentPhononScatteringKernel()
        r.id = id
        r.Ei = Ei
        r.phonons = phonons
        r.max_energy_transfer = max_energy_transfer
        r.max_momentum_transfer = max_momentum_transfer
        return r

    from Phonons import Phonons
    records = [
        k('polyxtalcoherentphononscatteringkernel-fccNi-0',
          'phonon-phonons-fccNi-0',
          70.,
          55.,
          12.5,
          ),
        ]

    for r in records: db.insertRow(r)
    return


def initids():
    return [
        'polyxtalcoherentphononscatteringkernel-fccNi-0',
        ]


# version
__id__ = "$Id$"

# End of file 
