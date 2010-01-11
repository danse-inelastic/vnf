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


from _ import PhononDispersion, AbstractScatteringKernel as base
class PolyXtalCoherentPhononScatteringKernel(base):

    dispersion = None
    Ei = 70.
    max_energy_transfer = 55.
    max_momentum_transfer = 12.5


    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = ['dispersion', 'Ei', 'max_energy_transfer', 'max_momentum_transfer']

        #
        def _createfield_for_dispersion(obj):
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
            referred_record = record.dispersion and record.dispersion.id \
                              and record.dispersion.dereference(self.orm.db)

            # widget
            doc = lc.document(Class='container', id='dispersion-selector-container')
            sp = doc.splitter()
            left = sp.section(); right = sp.section()
            #
            selector = FormSelectorField(label='Dispersion:', name='dispersion')
            left.add(selector)
            #
            plotcontainer = right.document(Class='container')
            #
            loadplot = lambda uid: load(
                actor='orm/phonondispersions', routine='createGraphicalView',
                uid=uid)

            # default selection
            if referred_record:
                value=orm.db.getUniqueIdentifierStr(referred_record)
            else:
                value=None

            # choices
            #  get matter
            matter = orm.db.dereference(record.matter)
            matterid = matter.id
            #  dynamically load choices
            entries = load(
                actor='orm/atomicstructures',
                routine='getSelectorEntriesForDispersion',
                id = matterid,
                include_none_entry = 1,
                )
            selector.oncreate = select(element=selector).setAttr(entries=entries, value=value)
            selector.onchange = select(element=plotcontainer).replaceContent(
                loadplot(select(element=selector).getAttr('value')))
            
            return doc

        drawer.mold._createfield_for_dispersion = _createfield_for_dispersion

    pass # end of PolyXtalCoherentPhononScatteringKernel



from _ import AbstractScatteringKernelInventory as InvBase
class Inventory(InvBase):
    
    dispersion = InvBase.d.reference(
        name='dispersion', targettype=PhononDispersion, owned=0)

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
    def k(id, dispersion, Ei, max_energy_transfer, max_momentum_transfer):
        r = PolyXtalCoherentPhononScatteringKernel()
        r.id = id
        r.Ei = Ei
        r.dispersion = dispersion
        r.max_energy_transfer = max_energy_transfer
        r.max_momentum_transfer = max_momentum_transfer
        return r

    from PhononDispersion import PhononDispersion
    records = [
        k('polyxtalcoherentphononscatteringkernel-fccNi-0',
          'phonon-dispersion-fccNi-0',
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
